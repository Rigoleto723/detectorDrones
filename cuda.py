import torch

# Verifica si CUDA (la API de GPU de NVIDIA) está disponible
if torch.cuda.is_available():
    # Obtiene el número de GPU disponibles
    num_gpus = torch.cuda.device_count()
    
    print(f"PyTorch está utilizando {num_gpus} GPU(s).")
    
    # Obtén información detallada de cada GPU
    for i in range(num_gpus):
        gpu_name = torch.cuda.get_device_name(i)
        print(f"GPU {i + 1}: {gpu_name}")
else:
    print("PyTorch no está utilizando GPU. Se está utilizando la CPU.")
