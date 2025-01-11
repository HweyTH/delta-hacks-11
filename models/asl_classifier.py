import tensorflow as tf
from tensorflow.python.keras import layers
from tensorflow.python.keras import models
from keras.src.legacy.preprocessing.image import ImageDataGenerator 

# Paths to data sets
train_dir = 'models/data/asl_alphabet_train'
test_dir = 'models/data/asl_alphabet_test'

# Parameters
img_size = (64,64)
batch_size = 32

# Data augmentation and preprocessing for training
train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2 # use 80 % for training and 20 % for validation
)

# Create training generator
train_generator = train_datagen.flow_from_directory(
    train_dir, 
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

# Create validation generator
validation_generator = train_datagen.flow_from_directory(
    train_dir, 
    target_size=img_size,
    batch_size=batch_size, 
    class_mode='categorical',
    subset='validation'
)

# Preprocess for testing data
test_datagen = ImageDataGenerator(rescale=1.0/225)

# Create testing generator
test_generator = test_datagen.flow_from_directory(
    test_dir, 
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical'
)

# Build the model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_size[0], img_size[1], 3)), 
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(len(train_generator.class_indices), activation='softmax')
])

# Compile the Model 
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the Model
history = model.fit(
    train_generator, 
    epochs=20,
    validation_data=validation_generator
)

# Evaluate on Test Data
test_loss, test_accuracy = model.evaluate(test_generator)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

# Save the Model
model.save('asl_language_classifier.h5')

# Map Class Indices to Labels
class_indices = train_generator.class_indices
label_map = {v: k for k, v in class_indices.items()}
print("Class Labels:", label_map)