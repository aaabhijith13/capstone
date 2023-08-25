import torch
import torch.nn as nn

# Assuming a simple LSTM model structure for the example
class SimpleLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim=1, num_layers=2):
        super(SimpleLSTM, self).__init__()
        self.hidden_dim = hidden_dim
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.linear(out[:, -1, :])
        return out

# Load the PyTorch model
def model_fn(model_dir):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleLSTM(...)  # Add your model parameters here
    with open(os.path.join(model_dir, "model.pth"), "rb") as f:
        model.load_state_dict(torch.load(f))
    return model.to(device)

# Deserialize the request payload
def input_fn(request_body, request_content_type):
    if request_content_type == "application/json":
        input_data = torch.tensor(json.loads(request_body), dtype=torch.float32)
        return input_data
    else:
        raise ValueError(f"Unsupported content type: {request_content_type}")

# Perform prediction
def predict_fn(input_data, model):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.eval()
    with torch.no_grad():
        input_data = input_data.to(device)
        output = model(input_data)
    return output.numpy()
