import torch

def benchmark_matrix_multiplication(matrix_size=1024, iterations=100):
    # GPU가 사용 가능한지 확인 (사용 불가능하면 CPU로 설정)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("사용 디바이스:", device)
    
    # 임의의 행렬 생성 (GPU/CPU에 할당)
    A = torch.randn(matrix_size, matrix_size, device=device)
    B = torch.randn(matrix_size, matrix_size, device=device)
    
    # 워밍업: 실제 벤치마크 전에 GPU 초기화를 위해 한번 수행
    C = torch.mm(A, B)
    if device.type == 'cuda':
        torch.cuda.synchronize()
    
    # GPU 이벤트를 사용하여 정밀한 시간 측정
    start_event = torch.cuda.Event(enable_timing=True)
    end_event = torch.cuda.Event(enable_timing=True)
    
    start_event.record()
    for i in range(iterations):
        C = torch.mm(A, B)
    end_event.record()
    
    # 모든 연산이 완료될 때까지 대기 (GPU 동기화)
    if device.type == 'cuda':
        torch.cuda.synchronize()
    
    # 총 소요 시간 (밀리초 단위)
    elapsed_time_ms = start_event.elapsed_time(end_event)
    avg_time_ms = elapsed_time_ms / iterations
    print(f"행렬 크기 {matrix_size}x{matrix_size}의 평균 곱셈 시간: {avg_time_ms:.4f} ms")
    
    # 행렬 곱셈의 총 부동소수점 연산 횟수: 2 * n^3 (대략)
    total_flops = 2 * (matrix_size ** 3)
    avg_time_sec = avg_time_ms / 1000.0
    gflops = (total_flops / avg_time_sec) / 1e9
    print(f"대략적인 성능: {gflops:.2f} GFLOPS")

if __name__ == "__main__":
    benchmark_matrix_multiplication()
