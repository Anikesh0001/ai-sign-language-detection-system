import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split

class SignLanguageModel:
    def __init__(self, input_shape=(64, 64, 3), num_classes=26):  # Default for ASL alphabet (A-Z)
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = self._build_model()

    def _build_model(self):
        model = models.Sequential([
            # CNN layers
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=self.input_shape),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            
            # Dense layers
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model

    def train(self, train_data, train_labels, validation_data=None, 
              batch_size=32, epochs=10):
        """
        Train the model on the provided dataset
        """
        # Data augmentation for training
        datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )

        # Convert labels to categorical
        train_labels_cat = tf.keras.utils.to_categorical(train_labels, self.num_classes)
        
        # Train the model
        history = self.model.fit(
            datagen.flow(train_data, train_labels_cat, batch_size=batch_size),
            epochs=epochs,
            validation_data=validation_data,
            verbose=1
        )
        
        return history

    def predict(self, image):
        """
        Predict the sign language class for a single image
        """
        # Ensure image has correct shape
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0)
        
        # Make prediction
        prediction = self.model.predict(image)
        return np.argmax(prediction[0])

    def save_model(self, path):
        """
        Save the trained model
        """
        self.model.save(path)

    @classmethod
    def load_model(cls, path):
        """
        Load a trained model
        """
        model = tf.keras.models.load_model(path)
        return model

def prepare_dataset(data_path, img_size=(64, 64)):
    """
    Prepare dataset from directory structure:
    data_path/
        class1/
            img1.jpg
            img2.jpg
            ...
        class2/
            img1.jpg
            img2.jpg
            ...
    """
    images = []
    labels = []
    class_names = sorted(os.listdir(data_path))
    
    for class_idx, class_name in enumerate(class_names):
        class_path = os.path.join(data_path, class_name)
        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            img = tf.keras.preprocessing.image.load_img(
                img_path, target_size=img_size
            )
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            images.append(img_array)
            labels.append(class_idx)
    
    return np.array(images), np.array(labels), class_names

def main():
    # Dataset path updated to 'backend/dataset' directory
    DATA_PATH = "backend/dataset"  # Dataset directory path
    IMG_SIZE = (64, 64)
    BATCH_SIZE = 32
    EPOCHS = 10
    
    # Load and prepare dataset
    X, y, class_names = prepare_dataset(DATA_PATH, IMG_SIZE)
    X = X / 255.0  # Normalize pixel values
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Initialize and train model
    model = SignLanguageModel(
        input_shape=(*IMG_SIZE, 3),
        num_classes=len(class_names)
    )
    
    # Train the model
    history = model.train(
        X_train,
        y_train,
        validation_data=(X_test, tf.keras.utils.to_categorical(y_test)),
        batch_size=BATCH_SIZE,
        epochs=EPOCHS
    )
    
    # Save the trained model
    model.save_model('backend/models/sign_language_model.h5')

if __name__ == "__main__":
    main()
