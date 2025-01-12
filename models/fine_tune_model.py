import tensorflow as tf
from tf_keras.models import load_model
from tf_keras.layers import Dense, Dropout
from tf_keras.models import Model
from tf_keras.applications import MobileNetV2
from tf_keras.preprocessing.image import ImageDataGenerator
from tf_keras.optimizers.legacy import Adam

# Load pre-trained model
trained_model_path = "sign_language_model.h5"
trained_model = load_model(trained_model_path)

# Extract the trained model without the top layers
trained_model.trainable = False  # Freeze the model weights

# Add new layers for fine-tuning
x = trained_model.output 
x = Dense(128, activation='relu', name="dense_128")(x)  # Add a unique name to the Dense layer
x = Dropout(0.3, name="dropout_0.3")(x)  # Add a unique name to the Dropout layer
output_layer = Dense(trained_model.output_shape[1], activation='softmax', name="output_layer")(x)  # Unique name for output layer

# Create a new model
model = Model(inputs=trained_model.input, outputs=output_layer)

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

# Paths to datasets
train_dir = 'models/data/ASL_Alphabet_Dataset/asl_alphabet_train'
test_dir = 'models/data/ASL_Alphabet_Dataset/asl_alphabet_test'

# Parameters
img_size = (64, 64)
batch_size = 32

# Data augmentation and preprocessing
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

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

# Fine-tune the model
# history = model.fit(
#     train_generator,
#     epochs=10,
#     steps_per_epoch=train_generator.samples // train_generator.batch_size,
#     validation_data=validation_generator,
#     validation_steps=validation_generator.samples // validation_generator.batch_size
# )

# Unfreeze some layers of the base model for fine-tuning
for layer in trained_model.layers[-30:]:
    layer.trainable = True

# Recompile with a lower learning rate for fine-tuning
model.compile(optimizer=Adam(learning_rate=1e-5), loss='categorical_crossentropy', metrics=['accuracy'])

# Further fine-tune the model
fine_tune_history = model.fit(
    train_generator,
    epochs=10,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size
)

# Save the fine-tuned model
model.save("fine_tuned_sign_language_model.keras")

# Evaluate the model on the test set
test_datagen = ImageDataGenerator(rescale=1.0 / 255)
test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=img_size,
    batch_size=1,
    class_mode='categorical'
)

test_loss, test_accuracy = model.evaluate(test_generator, steps=test_generator.samples)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")