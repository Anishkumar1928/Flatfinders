import React, { createContext, useState, useEffect } from 'react';
import { Alert } from 'react-native';
import * as Location from 'expo-location';
import AsyncStorage from '@react-native-async-storage/async-storage';


export const ContextApi = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [profile, setProfile] = useState({});
  const [roomdata, setRoomdata] = useState(null);
  const [pincode, setPincode] = useState('');
  const [roomsbypincode,setRoomsbypincode]=useState([])
  const [myproperty,setMyproperty]=useState([])


  useEffect(() => {
    const checkAuth = async () => {
      setLoading(true);
      try {
        const token = await AsyncStorage.getItem('access_token');
        token ? setIsAuthenticated(true) : setIsAuthenticated(false);
      } catch (error) {
        console.error('Error checking authentication:', error);
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };


    checkAuth();
  }, []);

  const login = async (mobile, password) => {
    if (!mobile || !password) {
      Alert.alert('Error', 'Mobile and password are required.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('https://flatfinders.vercel.app/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mobile, password }),
      });

      const responseText = await response.text();

      if (response.ok) {
        const data = JSON.parse(responseText);
        await AsyncStorage.setItem('access_token', data.access_token);
        setIsAuthenticated(true);
        Alert.alert('Success', 'Logged in successfully!');
      } else {
        const errorData = JSON.parse(responseText);
        Alert.alert('Error', errorData.msg || 'Login failed.');
      }
    } catch (error) {
      console.error('Login error:', error);
      Alert.alert('Error', 'An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    setLoading(true);
    try {
      await AsyncStorage.removeItem('access_token');
      setIsAuthenticated(false);
      Alert.alert('Success', 'Logged out successfully!');
    } catch (error) {
      console.error('Logout error:', error);
      Alert.alert('Error', 'An error occurred during logout.');
    } finally {
      setLoading(false);
    }
  };

  const fetchProfile = async () => {
    setLoading(true);
    try {
      const token = await AsyncStorage.getItem('access_token');
      if (!token) throw new Error('No token found');

      const response = await fetch(
        'https://flatfinders.vercel.app/getprofile',
        {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setProfile(data);
        setIsAuthenticated(true);
        console.log(data);
        setLoading(false);
      } else {
        const errorData = await response.json().catch(() => null);
        const errorMessage = errorData?.msg || `Error: ${response.status}`;
        console.error('Error fetching profile:', errorMessage);
        await logout();

        if (response.status === 401) {
          // Token expired or invalid
          await logout();
        }
      }
    } catch (error) {
      console.error('Fetch profile error:', error.message);
      await logout();
    } finally {
      setLoading(false);
    }
  };

  const fetchRoomDetails = async (room_id) => {
    try {
      const token = await AsyncStorage.getItem('access_token');
      const response = await fetch(
        'https://flatfinders.vercel.app/getproperty',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`, // Replace with your actual token
          },
          body: JSON.stringify({ property_id: room_id }),
        }
      );
      const result = await response.json();
      setRoomdata(result);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching property data:', err);
      
      setLoading(false);
    }
    
  };

async function getCurrentLocation() {
  try {
    let { status } = await Location.requestForegroundPermissionsAsync();
    if (status !== 'granted') {
      setErrorMsg('Permission to access location was denied');
      return;
    }

    let location = await Location.getCurrentPositionAsync({});
    const { latitude, longitude } = location.coords;

    console.log('Location:', latitude, longitude);

    const response = await fetch(
      `https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`,
      {
        headers: {
          'User-Agent': 'YourAppName/1.0 (contact@example.com)', // Use your details here
        },
      }
    );
    const data = await response.json();
    const postalCode = data.address?.postcode || 'Pin code not found';
    setPincode(postalCode);
    getpropertybypincode(postalCode)
    console.log(postalCode)
  } catch (error) {
    console.error('Error:', error.message);
    // setError(error.message || 'An unexpected error occurred');
  }
}
 
async function updatePassword(newPassword) {
  const url = "https://flatfinders.vercel.app/update_password"; // Replace with your actual API URL
  try {
    // Retrieve the JWT token from AsyncStorage
    const token = await AsyncStorage.getItem('access_token');
    
    if (!token) {
      console.error("No access token found. Please log in.");
      return;
    }

    // Make the API request to update the password
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}` // Include JWT token in headers
      },
      body: JSON.stringify({ new_password: newPassword }) // Payload with the new password
    });

    // Log the entire response to see what is returned
    const responseData = await response.json();
    console.log("API Response:", responseData); // Log the response data

    // Check if the response is valid and contains 'msg'
    if (response.ok) {
      console.log("Password updated successfully:", responseData.msg || "No message returned.");
      Alert.alert('Success', 'Password changed successfully!');
    } else {
      console.error("Error updating password:", responseData.msg || "Unknown error.");
      Alert.alert("Error updating password:", responseData.msg || "Unknown error.");
    }
  } catch (error) {
    // Log any errors during the fetch or processing
    console.error("An error occurred while updating the password:", error);
    Alert.alert("An error occurred while updating the password:", error);
  }
}

async function getpropertybypincode(pinCode){
     try {
      const token = await AsyncStorage.getItem('access_token');
      const response = await fetch(
        'https://flatfinders.vercel.app/getproperty',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`, // Replace with your actual token
          },
          body: JSON.stringify({ pin_code: pinCode }),
        }
      );
      const result = await response.json();
      setRoomsbypincode(result);
      console.log(result)
      setLoading(false);
    } catch (err) {
      console.error('Error fetching property data:', err);
      setLoading(false);
    } 
 
}

async function getpropertybyid(){
     try {
      const token = await AsyncStorage.getItem('access_token');
      console.log("myprprty")
      const response = await fetch(
        'https://flatfinders.vercel.app/getproperty',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`, // Replace with your actual token
          },
          body: JSON.stringify({}),
        }
      );
      const result = await response.json();
      setMyproperty(result);
      console.log(result)
      setLoading(false);
    } catch (err) {
      console.error('Error fetching property data:', err);
      setLoading(false);
    } 
 
}
  return (
    <ContextApi.Provider
      value={{
        isAuthenticated,
        login,
        logout,
        loading,
        error,
        setIsAuthenticated,
        setLoading,
        profile,
        setProfile,
        fetchProfile,
        setError,
        roomdata,
        fetchRoomDetails,
        getCurrentLocation,
        pincode, 
        setPincode,
        roomsbypincode,
        getpropertybypincode,
        myproperty,
        getpropertybyid,
        updatePassword
      }}>
      {children}
    </ContextApi.Provider>
  );
};
