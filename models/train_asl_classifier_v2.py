import tensorflow as tf
from tf_keras.models import Sequential
from tf_keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from tf_keras.utils import load_img, img_to_array
from tf_keras.models import load_model

# Paths to data sets
train_dir = 'models/data/ASL_Alphabet_Dataset/asl_alphabet_train'
test_dir = 'models/data/ASL_Alphabet_Dataset/asl_alphabet_test'

# Parameters
img_size = (160, 160)  # Resize all images to 160x160 for quicker processing
batch_size = 64  # Increased batch size to 64 for faster processing
epochs = 10  # Reduce the number of epochs to speed up training

# Data Augmentation and Preprocessing for Training
train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    rotation_range=20,  # Reduced rotation range
    width_shift_range=0.2,  # Reduced shift range
    height_shift_range=0.2,  # Reduced shift range
    shear_range=0.2,  # Reduced shear range
    zoom_range=0.2,  # Reduced zoom range
    horizontal_flip=True,
    validation_split=0.2  # allocate 20 percent for validation purpose
)

# Create Training and Validation Generators
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)

# Preprocessing for Testing Data
test_datagen = ImageDataGenerator(rescale=1.0/255)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=img_size,
    batch_size=1,  
    class_mode='categorical'
)

# Build the Model (slightly reduced complexity)
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_size[0], img_size[1], 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(len(train_generator.class_indices), activation='softmax')
])

# Compile the Model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the Model
history = model.fit(
    train_generator,
    epochs=epochs, 
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size
)

# Save the Model
model.save("sign_language_model_v2.h5")

# Evaluate on Test Data
test_loss, test_accuracy = model.evaluate(
    test_generator,
    steps=test_generator.samples // test_generator.batch_size
)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

# Map Class Indices to Labels
class_indices = train_generator.class_indices
label_map = {v: k for k, v in class_indices.items()}
print("Class Labels:", label_map)
