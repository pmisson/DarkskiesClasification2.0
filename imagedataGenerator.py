from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Generador de datos de entrenamiento con aumentación
train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2  # Dividir un porcentaje para validación
)

# Directorio de entrenamiento
train_dir = '/home/pmisson/Descargas/DarkskiesTrain/Alternate/inceptiosn_desde_0/train'

# Conjuntos de datos de entrenamiento y validación
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(299, 299),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(299, 299),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Sequential

base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(299, 299, 3))
base_model.trainable = False

model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(1024, activation='relu'),
    Dense(train_generator.num_classes, activation='softmax')  # Ajustar al número de clases detectadas
])

from tensorflow.keras.optimizers import RMSprop

model.compile(
    optimizer=RMSprop(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Entrenamiento inicial de las capas superiores
steps_per_epoch = train_generator.samples // train_generator.batch_size
validation_steps = validation_generator.samples // validation_generator.batch_size

history = model.fit(
    train_generator,
    steps_per_epoch=steps_per_epoch,
    epochs=10,
    validation_data=validation_generator,
    validation_steps=validation_steps
)

print(history.history.keys())  # Debería incluir 'val_loss' y 'val_accuracy'

base_model.trainable = True
for layer in base_model.layers[:-100]:  # Ajustar el número según las capas a liberar
    layer.trainable = False

# Recompilar con un learning rate más bajo para el ajuste fino
model.compile(
    optimizer=RMSprop(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

fine_tune_history = model.fit(
    train_generator,
    epochs=20,
    validation_data=validation_generator
)

model.save("inceptionV3_finetuned_darkskies.h5")

