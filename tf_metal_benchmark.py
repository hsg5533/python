import tensorflow as tf
import time

@tf.function
def matmul_fn(A, B):
    # tf.function으로 감싸서 그래프 모드로 실행
    return tf.matmul(A, B)

def benchmark_matrix_multiplication(sizes, dtype=tf.float32, num_runs=10, num_warmup=3):
    """
    행렬 곱셈 벤치마크:
      - sizes: 테스트할 행렬 크기 목록, 예) [512, 1024, 2048, ...]
      - dtype: tf.float32, tf.float16 등
      - num_runs: 측정 반복 횟수
      - num_warmup: 측정 전 워밍업 실행 횟수

    반환값: [(n, avg_elapsed_time, tflops), ...] 형태의 리스트
    """
    results = []
    
    for n in sizes:
        try:
            # 무작위 텐서 A, B 생성
            A = tf.random.uniform((n, n), dtype=dtype)
            B = tf.random.uniform((n, n), dtype=dtype)
            
            # 워밍업: 여러 번 실행해서 초기화 비용 제거
            for _ in range(num_warmup):
                C = matmul_fn(A, B)
                _ = tf.reduce_sum(C).numpy()
            
            # 측정: 여러 번 실행 후 평균 시간 산출
            times = []
            for _ in range(num_runs):
                start_time = time.perf_counter()
                C = matmul_fn(A, B)
                # 동기화: 결과를 .numpy()로 가져와 연산이 끝날 때까지 기다림
                _ = tf.reduce_sum(C).numpy()
                end_time = time.perf_counter()
                times.append(end_time - start_time)
            
            avg_time = sum(times) / len(times)
            
            # 총 연산 FLOPs: 행렬 곱셈은 대략 2*n^3 FLOPs
            flops = 2.0 * (n ** 3)
            tflops = flops / (avg_time * 1e12)
            
            results.append((n, avg_time, tflops))
        
        except tf.errors.ResourceExhaustedError:
            print(f"OOM 발생! {n} x {n} (dtype={dtype}) 크기는 건너뜁니다.")
            continue

    return results

def main():
    # GPU 확인
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print("Using Apple GPU for TensorFlow (Metal) benchmarking.\n")
    else:
        print("No GPU found, running on CPU.\n")
    
    # 테스트할 행렬 크기 목록 (필요 시 수정)
    test_sizes = [512, 1024, 2048, 4096, 8192, 16384, 32768]
    
    dtype = tf.float32
    print(f"Using dtype: {dtype}")

    results = benchmark_matrix_multiplication(test_sizes, dtype=dtype, num_runs=10, num_warmup=3)
    
    print("TensorFlow-Metal Matrix Multiplication Benchmark (TFLOPS)")
    print("==========================================================")
    max_tflops = 0.0
    for (n, avg_time, tf_) in results:
        print(f"Size = {n:5d} x {n:5d} | Avg Time = {avg_time:.6f} s | TFLOPS = {tf_:.4f}")
        if tf_ > max_tflops:
            max_tflops = tf_
    print(f"\nBenchmark Score (Max TFLOPS) = {max_tflops:.4f}")

if __name__ == "__main__":
    main()