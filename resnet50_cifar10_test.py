import tensorflow as tf
import numpy as np
import time

###############################
# 0. 환경 및 디바이스 확인
###############################
# Apple Silicon(GPU) 디바이스가 잡히는지 확인
physical_gpus = tf.config.list_physical_devices('GPU')
print("인식된 GPU 디바이스:", physical_gpus)

###############################
# 1. CIFAR-10 데이터셋 로드
###############################
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

print("원본 x_train 크기:", x_train.shape, "원본 x_test 크기:", x_test.shape)
print("원본 y_train 크기:", y_train.shape, "원본 y_test 크기:", y_test.shape)

num_classes = 10

###############################
# 2. 이미지 리사이즈 (32→224)
###############################
# ResNet50은 224 x 224 x 3 입력이 기본
new_size = (224, 224)

# 정규화(0~1 범위) 후 리사이즈
x_train_resized = tf.image.resize(x_train / 255.0, new_size)
x_test_resized  = tf.image.resize(x_test / 255.0, new_size)

# Tensor 형태로 변환
x_train_resized = tf.convert_to_tensor(x_train_resized, dtype=tf.float32)
x_test_resized  = tf.convert_to_tensor(x_test_resized, dtype=tf.float32)

###############################
# 3. 라벨(정답) 변환
###############################
# CIFAR-10 라벨은 (배치, 1) 형태, one-hot으로 바꾸지 않고
# 그냥 sparse_categorical_crossentropy 사용 가능
y_train = y_train.reshape(-1)
y_test = y_test.reshape(-1)

###############################
# 4. 모델 정의 (ResNet50)
###############################
def create_model():
    # Keras 응용 프로그램(ResNet50) 사용
    # include_top=True 로 ImageNet 분류 헤더를 쓰지만,
    # 최종 클래스 수를 CIFAR-10에 맞게 조정하려면 include_top=False 후 직접 Dense를 달아도 됩니다.
    # 여기서는 ResNet50을 ImageNet 분류 헤더까지 포함시키고,
    # 마지막 Dense만 새로 설정하는 방법(Functional API)을 예시로 보여드리겠습니다.
    
    # 1) base 모델 (ImageNet 가중치 로드, 최종 Dense 제외)
    base_model = tf.keras.applications.ResNet50(
        weights='imagenet',  # ImageNet 사전학습 가중치
        include_top=False,   # 분류기 부분 제외
        input_shape=(224, 224, 3)
    )
    
    # 2) GlobalAveragePooling 등으로 펼친 후, 새 Dense 레이어 추가
    x = base_model.output
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(1024, activation='relu')(x)
    outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)

    model = tf.keras.Model(inputs=base_model.input, outputs=outputs)
    
    # 모든 레이어를 학습 가능하게 설정 (ResNet50 전체 fine-tuning)
    for layer in base_model.layers:
        layer.trainable = True
    
    # optimizer, loss 설정
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

###############################
# 5. CPU에서 학습 테스트
###############################
cpu_model = create_model()
start_time_cpu = time.time()

print("\n[CPU 학습 시작]")
with tf.device('/CPU:0'):
    history_cpu = cpu_model.fit(
        x_train_resized, y_train,
        epochs=2,
        batch_size=32,
        validation_split=0.1,
        verbose=1
    )

end_time_cpu = time.time()
cpu_time = end_time_cpu - start_time_cpu

print(f"CPU 학습 완료! 소요 시간: {cpu_time:.2f}초")

###############################
# 6. GPU에서 학습 테스트
###############################
if physical_gpus:
    gpu_model = create_model()
    start_time_gpu = time.time()

    print("\n[GPU 학습 시작]")
    with tf.device('/GPU:0'):
        history_gpu = gpu_model.fit(
            x_train_resized, y_train,
            epochs=2,
            batch_size=32,
            validation_split=0.1,
            verbose=1
        )

    end_time_gpu = time.time()
    gpu_time = end_time_gpu - start_time_gpu

    print(f"GPU 학습 완료! 소요 시간: {gpu_time:.2f}초")
else:
    gpu_time = None
    print("\nGPU가 감지되지 않아 GPU 학습 테스트를 진행하지 않았습니다.")

###############################
# 7. 결과 비교 및 테스트 평가
###############################
print("\n===== 학습 시간 비교 =====")
print(f"CPU  : {cpu_time:.2f}초")
if gpu_time:
    print(f"GPU  : {gpu_time:.2f}초")

# 최종 모델 정확도 (GPU 학습 모델이 있으면 해당 모델로 평가)
if gpu_time:
    loss_gpu, acc_gpu = gpu_model.evaluate(x_test_resized, y_test, verbose=0)
    print(f"\n[GPU 모델 테스트 성능] loss={loss_gpu:.4f}, accuracy={acc_gpu:.4f}")
else:
    loss_cpu, acc_cpu = cpu_model.evaluate(x_test_resized, y_test, verbose=0)
    print(f"\n[CPU 모델 테스트 성능] loss={loss_cpu:.4f}, accuracy={acc_cpu:.4f}")