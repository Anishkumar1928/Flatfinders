import React, { useState ,useContext} from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert, StyleSheet, ActivityIndicator, Image } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { ContextApi } from './ContextApi';

export default function UpdateProfile({ navigation }) {
  const { profile} = useContext(ContextApi);
  const [name, setName] = useState(profile?.logged_in_as?.[1]);
  const [mobile, setMobile] = useState(String(profile?.logged_in_as?.[2] || ''));
  const [email, setEmail] = useState(profile?.logged_in_as?.[3]);
  const [gender, setGender] = useState(profile?.logged_in_as?.[5]);
  const [role, setRole] = useState(profile?.logged_in_as?.[6]);
  const [profilePic, setProfilePic] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpdateProfile = async () => {
    if (!name || !mobile || !email || !gender || !role) {
      Alert.alert('Error', 'Please fill in all the fields.');
      return;
    }

    setLoading(true);
    const token = await AsyncStorage.getItem('access_token');

    try {
      const formData = new FormData();
      if (profilePic) {
        const imageUri = profilePic;
        const filename = imageUri.split('/').pop();
        const match = /\.(\w+)$/.exec(filename);
        const type = match ? `image/${match[1]}` : 'image';

        formData.append('file', {
          uri: imageUri,
          name: filename,
          type,
        });
      }

      formData.append('name', name);
      formData.append('mobile', mobile);
      formData.append('email', email);
      formData.append('gender', gender);
      formData.append('role', role);

      const response = await fetch('https://flatfinders.vercel.app/update_profile', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`, 
          'Content-Type': 'multipart/form-data',
        },
        body: formData,
      });

      const data = await response.json();

      if (response.status === 200) {
        Alert.alert('Success', 'Profile updated successfully!');
        navigation.navigate('Home') // Navigate back after successful update
      } else {
        Alert.alert('Error', data.msg || 'Profile update failed.');
      }
    } catch (error) {
      console.error('Profile update error:', error);
      Alert.alert('Error', 'An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleImagePicker = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.All,
      allowsEditing: true,
      aspect: [4, 4],
      quality: 1,
    });

    if (!result.canceled) {
      setProfilePic(result.assets[0].uri);
    }

  };

  return (
    <View style={styles.container}>
      {/* Profile Picture Section */}
      <TouchableOpacity style={styles.imagePicker} onPress={handleImagePicker}>
        {profilePic ? (
          <Image source={{ uri: profilePic }} style={styles.image} />
        ) : (
          <Text style={styles.imagePlaceholder}>Pick a Profile Picture</Text>
        )}
      </TouchableOpacity>

      <Text style={styles.label}>Name</Text>
      <TextInput
        style={styles.input}
        placeholder="Name"
        value={name}
        onChangeText={setName}
      />
      <Text style={styles.label}>Mobile</Text>
      <TextInput
        style={styles.input}
        placeholder="Mobile"
        value={mobile}
        onChangeText={setMobile}
        keyboardType="numeric"
      />
      <Text style={styles.label}>Email</Text>
      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
      />


      <Text style={styles.label}>Gender</Text>
      <View style={styles.radioContainer}>
        <TouchableOpacity style={styles.radioButton} onPress={() => setGender('M')}>
          <View style={gender === 'M' ? styles.radioSelected : styles.radio} />
          <Text style={styles.radioText}>Male</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.radioButton} onPress={() => setGender('F')}>
          <View style={gender === 'F' ? styles.radioSelected : styles.radio} />
          <Text style={styles.radioText}>Female</Text>
        </TouchableOpacity>
      </View>

      <Text style={styles.label}>Role</Text>
      <View style={styles.radioContainer}>
        <TouchableOpacity style={styles.radioButton} onPress={() => setRole('Renter')}>
          <View style={role === 'Renter' ? styles.radioSelected : styles.radio} />
          <Text style={styles.radioText}>Renter</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.radioButton} onPress={() => setRole('Owner')}>
          <View style={role === 'Owner' ? styles.radioSelected : styles.radio} />
          <Text style={styles.radioText}>Owner</Text>
        </TouchableOpacity>
      </View>

      <TouchableOpacity style={styles.button} onPress={handleUpdateProfile} disabled={loading}>
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>UpdateProfile</Text>
        )}
      </TouchableOpacity>

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f2f2f2',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  imagePicker: {
    width: 100,
    height: 100,
    borderRadius: 50,
    borderWidth: 2,
    borderColor: '#000',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
  },
  image: {
    width: '100%',
    height: '100%',
    borderRadius: 50,
  },
  imagePlaceholder: {
    textAlign: 'center',
    color: '#000',
  },
  input: {
    width: '100%',
    padding: 15,
    marginVertical: 10,
    backgroundColor: '#fff',
    borderRadius: 10,
  },
  label: {
    alignSelf: 'flex-start',
    marginTop: 10,
    marginBottom: 5,
    fontWeight: 'bold',
  },
  radioContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
    marginBottom: 15,
  },
  radioButton: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  radio: {
    height: 20,
    width: 20,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: '#000',
    marginRight: 10,
  },
  radioSelected: {
    height: 20,
    width: 20,
    borderRadius: 10,
    backgroundColor: '#000',
    marginRight: 10,
  },
  radioText: {
    fontSize: 16,
  },
  button: {
    backgroundColor: 'black',
    padding: 15,
    borderRadius: 10,
    width: '100%',
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
  },

});
