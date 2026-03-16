import time
import torch
import torch._dynamo as dynamo
import torchvision.models as models

print(torch.__version__)


def foo(x, y):
    a = torch.sin(x)
    b = torch.cos(y)
    return a + b

start = time.time()
out = foo(torch.randn(10,10), torch.randn(10,10))

# compiled_model = torch.compile(foo)
# out = compiled_model(torch.randn(10,10), torch.randn(10,10))

# compiled_model = dynamo.optimize("inductor")(foo)
# out = compiled_model(torch.randn(10,10), torch.randn(10,10))
end = time.time()
print("Compile time:", end - start)

#####################################

model = models.resnet18()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
compiled_model = dynamo.optimize("inductor")(model)

x = torch.randn(16, 3, 224, 224)
optimizer.zero_grad()

count = []
for epoch in range(10):
    start = time.time()
    out  = compiled_model(x)
    out.sum().backward()
    optimizer.step()
    end = time.time()
    count.append(end-start)
    print("Finished Training: ", end-start)

print(sum(count)/len(count))
