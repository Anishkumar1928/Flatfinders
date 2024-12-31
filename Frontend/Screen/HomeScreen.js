import React, { useState, useEffect, useContext } from 'react';
import {
  View,
  Text,
  TextInput,
  ScrollView,
  Image,
  TouchableOpacity,
  StyleSheet,
  Alert,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { ContextApi } from './ContextApi';
import LoadingScreen from './LoadingScreen';
import ErrorScreen from './ErrorScreen';
import Roomnotfound from './Roomnotfound'

export default function HomeScreen({ navigation }) {
  // Store the profile data
  const {
    loading,
    profile,
    fetchProfile,
    error,
    pincode,
    setPincode,
    getCurrentLocation,
    roomsbypincode,
    getpropertybypincode,
  } = useContext(ContextApi);

  useEffect(() => {
    fetchProfile();
  }, []);

  useEffect(() => {
    const fetchLocation = async () => {
      await getCurrentLocation();
    };

    fetchLocation();
  }, []);

  if (loading) {
    return <LoadingScreen />;
  }

  if (error) {
    return <ErrorScreen />;
  }

  function fetchProperties() {}

  return (
    <>
      <View style={styles.container}>
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>
              Hello, {profile?.logged_in_as?.[1] || 'Guest'}
            </Text>

            <Text style={styles.title}>Find your ideal room</Text>
          </View>
          <TouchableOpacity
            onPress={() => navigation.navigate('ProfileScreen')}>
            {' '}
            >
            <Image
              source={{
                uri:
                  profile?.profilpic ||
                  'https://images.unsplash.com/photo-1536494126589-29fadf0d7e3c?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8cm9vbXxlbnwwfHwwfHx8MA%3D%3D',
              }}
              style={styles.avtar}
            />
          </TouchableOpacity>
        </View>

        <View style={styles.searchContainer}>
          <TextInput
            keyboardType="numeric"
            maxLength={6}
            onChangeText={(text) => setPincode(text)}
            placeholder="pincode"
            value={pincode}
            onSubmitEditing={() => getpropertybypincode(pincode)}
            editable={!loading} // Disable input while loading
            style={styles.searchInput}
          />
        </View>

        <ScrollView>
          {/* Local Listings */}
          <Text style={styles.sectionTitle}>Local listings</Text>
          <View style={styles.listingsGrid}>
            {roomsbypincode.length > 0 ? (
              roomsbypincode.map((room) => (
                <TouchableOpacity
                  key={room.property_details[0][0]}
                  style={styles.listingCard}
                  onPress={() => {
                    navigation.navigate('RoomDetails', { room });
                  }}>
                  <Image
                    source={{ uri: room.property_photos[0][2] }}
                    style={styles.listingImage}
                  />
                  <Text style={styles.listingTitle}>
                    {room.property_details[2]}
                  </Text>
                  <Text style={styles.listingSubtitle}>
                    {room.property_details[3]}/month
                  </Text>
                  <Text style={styles.listingSubtitle}>
                    {room.property_details[4]}
                  </Text>
                </TouchableOpacity>
              ))
            ) : (
              <Roomnotfound text={"NOT FOUND"}/>
            )}
          </View>
        </ScrollView>
      </View>
      }
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
    paddingHorizontal: 16,
  },
  header: {
    marginTop: 40,
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  avtar: {
    height: 50,
    width: 50,
    borderRadius: 50,
  },
  greeting: {
    fontSize: 18,
    fontWeight: '300',
    color: '#555',
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: '#000',
    marginBottom: 16,
  },
  searchContainer: {
    marginBottom: 20,
  },
  searchInput: {
    height: 50,
    borderColor: '#CCC',
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: 16,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    marginTop: 20,
    marginBottom: 10,
  },
  featuredCard: {
    flexDirection: 'row',
    marginBottom: 16,
    backgroundColor: '#FFF',
    borderRadius: 8,
    overflow: 'hidden',
  },
  roomImage: {
    width: 100,
    height: 100,
  },
  roomInfo: {
    flex: 1,
    padding: 10,
    justifyContent: 'center',
  },
  roomTitle: {
    fontSize: 16,
    fontWeight: '600',
  },
  roomSubtitle: {
    fontSize: 12,
    color: '#777',
    marginVertical: 4,
  },
  viewButton: {
    backgroundColor: '#000',
    padding: 8,
    borderRadius: 4,
    alignSelf: 'flex-start',
  },
  viewButtonText: {
    color: '#FFF',
    fontWeight: '600',
  },
  listingsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  listingCard: {
    width: '48%',
    marginBottom: 16,
  },
  listingImage: {
    width: '100%',
    height: 120,
    borderRadius: 8,
  },
  listingTitle: {
    fontSize: 14,
    fontWeight: '600',
    marginTop: 8,
  },
  listingSubtitle: {
    fontSize: 12,
    color: '#777',
  },
});
