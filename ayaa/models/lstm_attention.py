import pandas as pd
import numpy as np
import torch
from sklearn.preprocessing import StandardScaler

# 加载A股数据（示例特征）
data = pd.read_csv('../data_source/stock_data.csv', parse_dates=['date'])
features = ['open', 'high', 'low', 'close', 'volume']  # 基础特征+技术指标[8]

# 添加技术指标（示例）
data['MA5'] = data['close'].rolling(5).mean()
# data['RSI'] = compute_rsi(data['close'])  # 自定义计算函数[8]

# 数据清洗
data.dropna(inplace=True)
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data[features])
print(scaled_data)

# 构建时序样本（窗口长度建议30-60天[7]）
def create_sequences(data, seq_length=30, pred_length=1):
    X, y = [], []
    for i in range(len(data)-seq_length-pred_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length:i+seq_length+pred_length, 3])  # 预测收盘价[5]
    return torch.FloatTensor(np.array(X)), torch.FloatTensor(np.array(y))

X, y = create_sequences(scaled_data)
print('total X: {}, total y: {}'.format(len(X), len(y)))


import torch.nn as nn

class StockLSTMAttention(nn.Module):
    def __init__(self, input_dim=7, hidden_dim=64, n_layers=2, output_dim=1):
        super().__init__()
        # 双向LSTM捕捉双向时序特征[9]
        self.lstm = nn.LSTM(input_dim, hidden_dim, n_layers, 
                          bidirectional=True, batch_first=True)
        # 注意力机制层
        self.attn = nn.Sequential(
            nn.Linear(2*hidden_dim, 64),  # 双向维度翻倍
            nn.Tanh(),
            nn.Linear(64, 1, bias=False)
        )
        # 预测层（考虑加入Dropout防过拟合[7]）
        self.fc = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(2*hidden_dim, output_dim)
        )

    def forward(self, x):
        lstm_out, _ = self.lstm(x)  # (batch, seq_len, 2*hidden)
        
        # 时间步注意力权重计算[3]
        attn_weights = torch.softmax(self.attn(lstm_out).squeeze(2), dim=1)
        context = torch.bmm(attn_weights.unsqueeze(1), lstm_out).squeeze(1)
        
        return self.fc(context)

from torch.utils.data import DataLoader, TensorDataset
import numpy

# 数据集划分（保持时序性）
train_ratio, val_ratio = 0.7, 0.15
train_size = int(len(X)*train_ratio)
val_size = int(len(X)*val_ratio)
print(f'train_size:{train_size}, val_size:{val_size}')

train_X, train_y = X[:train_size], y[:train_size]
val_X, val_y = X[train_size:train_size+val_size], y[train_size:train_size+val_size]
test_X, test_y = X[train_size+val_size:], y[train_size+val_size:]

train_X, train_y = X, y

# 数据加载器
batch_size = 64
train_loader = DataLoader(TensorDataset(train_X, train_y), 
                         batch_size=batch_size, shuffle=False)  # 时序数据禁止打乱[8]

# 模型初始化
model = StockLSTMAttention(input_dim=len(features))
print(model)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001, 
                            weight_decay=1e-5)  # L2正则化[7]

# 早停机制
best_loss = float('inf')
patience, counter = 10, 0

if torch.cuda.is_available():
    print(torch.cuda.current_device())
    print(torch.cuda.get_device_name(0))

cor_data = numpy.array([])
for epoch in range(200):
    # 训练阶段
    model.train()
    for batch_X, batch_y in train_loader:
        preds = model(batch_X)
        loss = criterion(preds, batch_y)

        if epoch == 1:
            # print(batch_X, batch_y, preds, loss)
            # print(batch_y.expand(preds))
            d = (batch_y - preds)/batch_y
            c = d.detach().cpu().numpy()
            cor_data = numpy.concatenate([cor_data, c[:,0]])
            # print(max(d), min(d))
            # print(c[:,0])

        optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), 1.0)  # 梯度裁剪[6]
        optimizer.step()
    
    if epoch == 1:
        print(len(cor_data))
        print(cor_data)

    # 验证阶段
    model.eval()
    with torch.no_grad():
        val_preds = model(val_X)
        val_loss = criterion(val_preds, val_y)
        
    if epoch % 20 == 0:
        print(f'epoch:{epoch} val_loss:{val_loss}')



    # # 早停判断
    # if val_loss < best_loss:
    #     best_loss = val_loss
    #     counter = 0
    #     torch.save(model.state_dict(), 'best_model.pth')
    # else:
    #     counter += 1
    #     if counter >= patience:
    #         print(f'Early stopping at epoch {epoch}')
    #         # break


# 输入最近N天数据 (需预处理)
data = pd.read_csv('../data_source/stock_data.csv', parse_dates=['date'])
scaled_data = scaler.fit_transform(data[features])
last_30_days = scaled_data[-31:-1]  
input_tensor = torch.FloatTensor(last_30_days).unsqueeze(0)

# 预测
model.eval()
with torch.no_grad():
    pred = model(input_tensor)
    print(pred)
    pred_price = scaler.inverse_transform(
        np.zeros((1,5)) + pred.item())[0][3]  # 反标准化

print(f"预测明日收盘价: {pred_price:.2f}")