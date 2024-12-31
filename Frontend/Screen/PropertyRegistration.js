import React, { useState ,useContext} from "react";
import AsyncStorage from '@react-native-async-storage/async-storage';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Image,
  Alert,
} from "react-native";
import { Picker } from "@react-native-picker/picker";
import * as ImagePicker from "expo-image-picker";
import { ContextApi } from './ContextApi';
import LoadingScreen from './LoadingScreen'

export default function PropertyRegistration({ navigation }) {
  const [formData, setFormData] = useState({
    propertyType: "Flat",
    rent: "",
    address: "",
    pinCode: "",
    dimensions: "",
    accommodation: "OnlyGirls",
    isParking: false,
    isKitchen: false,
    images: [],
  });

    const {
    setLoading,loading
  } = useContext(ContextApi);

  // Handle Input Change
  const handleInputChange = (key, value) => {
    setFormData({ ...formData, [key]: value });
  };

  // Handle Image Upload
  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsMultipleSelection: true,
    });

    if (!result.canceled) {
      setFormData({
        ...formData,
        images: [...formData.images, ...result.assets.map((asset) => asset.uri)],
      });
    }
  };



  // Submit Form Data
  const handleSubmit = async () => {
    setLoading(true)
    if (!formData.rent || !formData.address || !formData.pinCode) {
      Alert.alert("Error", "Please fill all required fields.");
      return;
    }

    const formPayload = new FormData();
    Object.keys(formData).forEach((key) => {
      if (key === "images") {
        formData.images.forEach((uri, index) => {
          formPayload.append("images", {
            uri,
            name: `image_${index}.jpg`,
            type: "image/jpeg",
          });
        });
      } else {
        formPayload.append(key, formData[key]);
      }
    });

    try {
      
      const token = await AsyncStorage.getItem('access_token');
      const response = await fetch("https://flatfinders.vercel.app/property", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`, // Replace with your JWT token logic
        },
        body: formPayload,
      });

      const result = await response.json();
      if (response.ok) {
        setLoading(false)
        Alert.alert("Success", "Property registered successfully!");
        setFormData({
          propertyType: "Flat",
          rent: "",
          address: "",
          pinCode: "",
          dimensions: "",
          accommodation: "OnlyGirls",
          isParking: false,
          isKitchen: false,
          images: [],
        });
        navigation.navigate('MypropertyScreen') 
      } else {
        setLoading(false)
        Alert.alert("Error", result.error || "Something went wrong.");
      }
    } catch (error) {
      setLoading(false)
      Alert.alert("Error", "An unexpected error occurred.");
      console.error("Error submitting form:", error);
    }
  };

  if(loading){
    return <LoadingScreen />
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>


      {/* Property Type */}
      <Text style={styles.label}>Property Type</Text>
      <View style={styles.pickerContainer}>
        <Picker
          selectedValue={formData.propertyType}
          onValueChange={(value) => handleInputChange("propertyType", value)}
        >
          <Picker.Item label="Flat" value="Flat" />
          <Picker.Item label="Room" value="Room" />
        </Picker>
      </View>

      {/* Rent */}
      <Text style={styles.label}>Rent (Per month ₹)</Text>
      <TextInput
        style={styles.input}
        keyboardType="numeric"
        value={formData.rent}
        onChangeText={(value) => handleInputChange("rent", value)}
      />

      {/* Address */}
      <Text style={styles.label}>Address</Text>
      <TextInput
        style={styles.input}
        value={formData.address}
        onChangeText={(value) => handleInputChange("address", value)}
      />


      {/* PIN Code */}
      <Text style={styles.label}>PIN Code</Text>
      <TextInput
        style={styles.input}
        keyboardType="numeric"
        minLength={6}
        maxLength={6}
        value={formData.pinCode}
        onChangeText={(value) => handleInputChange("pinCode", value)}
      />

      {/* Dimensions */}
      <Text style={styles.label}>Dimensions (sq. ft.)</Text>
      <TextInput
        style={styles.input}
        keyboardType="numeric"
        value={formData.dimensions}
        onChangeText={(value) => handleInputChange("dimensions", value)}
      />

      {/* Accommodation */}
      <Text style={styles.label}>Accommodation</Text>
      <View style={styles.pickerContainer}>
        <Picker
          selectedValue={formData.accommodation}
          onValueChange={(value) => handleInputChange("accommodation", value)}
        >
          <Picker.Item label="Only Girls" value="OnlyGirls" />
          <Picker.Item label="Only Boys" value="OnlyBoys" />
          <Picker.Item label="Only Family" value="OnlyFamily" />
          <Picker.Item label="Family and Girls" value="FamilyAndGirls" />
          <Picker.Item label="Both" value="Both" />
        </Picker>
      </View>

      {/* Parking Available */}
      <Text style={styles.label}>Is Parking Available?</Text>
      <View style={styles.radioContainer}>
        <TouchableOpacity
          style={styles.radioButton}
          onPress={() => handleInputChange("isParking", true)}
        >
          <View style={[styles.radioCircle, formData.isParking && styles.radioSelected]} />
          <Text>Yes</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.radioButton}
          onPress={() => handleInputChange("isParking", false)}
        >
          <View style={[styles.radioCircle, !formData.isParking && styles.radioSelected]} />
          <Text>No</Text>
        </TouchableOpacity>
      </View>

      {/* Kitchen Available */}
      <Text style={styles.label}>Is Kitchen Available?</Text>
      <View style={styles.radioContainer}>
        <TouchableOpacity
          style={styles.radioButton}
          onPress={() => handleInputChange("isKitchen", true)}
        >
          <View style={[styles.radioCircle, formData.isKitchen && styles.radioSelected]} />
          <Text>Yes</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.radioButton}
          onPress={() => handleInputChange("isKitchen", false)}
        >
          <View style={[styles.radioCircle, !formData.isKitchen && styles.radioSelected]} />
          <Text>No</Text>
        </TouchableOpacity>
      </View>

      {/* Image Upload Section */}
      <Text style={styles.label}>Upload Images</Text>
      <TouchableOpacity style={styles.button} onPress={pickImage}>
        <Text style={styles.buttonText}>Select Images</Text>
      </TouchableOpacity>
      <ScrollView horizontal style={styles.imageContainer}>
        {formData.images.map((uri, index) => (
          <Image key={index} source={{ uri }} style={styles.image} />
        ))}
      </ScrollView>

      {/* Submit Button */}
      <TouchableOpacity style={styles.submitButton} onPress={handleSubmit}>
        <Text style={styles.submitButtonText}>Register</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    paddingTop: 60,
    backgroundColor: "#F5F5F5",
  },
  label: {
    fontWeight: "bold",
    marginBottom: 5,
    color: "#555",
  },
  input: {
    width: '100%',
    padding: 15,
    marginVertical: 10,
    backgroundColor: '#fff',
    borderRadius: 10,
  },
  pickerContainer: {
    width: '100%',
    padding: 5,
    marginVertical: 10,
    backgroundColor: '#fff',
    borderRadius: 10,
  },
  button: {
    backgroundColor: "#000",
    padding: 10,
    borderRadius: 5,
    alignItems: "center",
    marginBottom: 15,
  },
  buttonText: {
    color: "#fff",
    fontWeight: "bold",
  },
  imageContainer: {
    flexDirection: "row",
    marginBottom: 15,
  },
  image: {
    width: 100,
    height: 100,
    borderRadius: 5,
    marginRight: 10,
  },
  submitButton: {
    backgroundColor: "#000",
    padding: 15,
    borderRadius: 5,
    alignItems: "center",
  },
  submitButtonText: {
    color: "#fff",
    fontWeight: "bold",
    fontSize: 16,
  },
  radioContainer: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-around",
    marginBottom: 15,
  },
  radioButton: {
    flexDirection: "row",
    alignItems: "center",
    marginRight: 20,
  },
  radioCircle: {
    height: 20,
    width: 20,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "#ccc",
    alignItems: "center",
    justifyContent: "center",
    marginRight: 5,
  },
  radioSelected: {
    backgroundColor: "#000",
  },
});
