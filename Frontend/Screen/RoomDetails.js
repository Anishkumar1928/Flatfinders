import React, { useContext,useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Image,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import LoadingScreen from './LoadingScreen';
import ErrorScreen from './ErrorScreen';
import { ContextApi } from './ContextApi';

const RoomDetails = ({ route }) => {
  const { loading, error,setLoading } = useContext(ContextApi);
  const { room } = route.params;

  const handleContactOwner = () => {
    Alert.alert("Contact Owner", "You can contact the owner at +1 234-567-890.");
  };

  if (loading) {
    return <LoadingScreen />;
  }

  if (error) {
    return <ErrorScreen />;
  }


  return (
    <ScrollView style={styles.container}>
      {/* Image Carousel */}
      <View style={{ padding: 10 }}>
        <ScrollView horizontal style={styles.imageContainer}>
          {room.property_photos.length ? (
            room.property_photos.map((image, index) => (
              <Image
                key={index}
                source={{ uri: image[2] }}
                style={[
                  styles.image,
                  index !== room.property_photos.length - 1 && styles.imageMargin,
                ]}
              />
            ))
          ) : (
            <Text style={styles.placeholderText}>No Photos Available</Text>
          )}
        </ScrollView>
      </View>

      {/* Details Section */}
      <View style={styles.detailsContainer}>
        <Text style={styles.title}>{room.property_details[2]}</Text>
        <Text style={styles.rent}>₹{room.property_details[3]}/Month</Text>
        <Text style={styles.address}>{room.property_details[4]}</Text>
        <Text style={styles.pinCode}>PIN Code: {room.property_details[5]}</Text>
        <Text style={styles.dimensions}>
          Dimensions: {room.property_details[6]} sqft
        </Text>
        <Text style={styles.accommodation}>
          Accommodation: {room.property_details[7]}
        </Text>
      </View>

      {/* Amenities Section */}
      <View style={styles.amenitiesContainer}>
        <Text style={styles.sectionHeader}>Amenities</Text>
        <View style={styles.amenitiesList}>
          <View style={styles.amenity}>
            <MaterialIcons
              name={room.property_details[8] ? "home" : "block"}
              size={24}
              color={room.property_details[8] ? "green" : "red"}
            />
            <Text style={styles.amenityText}>
              {room.property_details[8] ? "Available" : "Occupied"}
            </Text>
          </View>
          <View style={styles.amenity}>
            <MaterialIcons
              name="local-parking"
              size={24}
              color={room.property_details[9] ? "green" : "red"}
            />
            <Text style={styles.amenityText}>
              {room.property_details[9] ? "Parking Available" : "No Parking"}
            </Text>
          </View>
          <View style={styles.amenity}>
            <MaterialIcons
              name="kitchen"
              size={24}
              color={room.property_details[10] ? "green" : "red"}
            />
            <Text style={styles.amenityText}>
              {room.property_details[10] ? "Kitchen Available" : "No Kitchen"}
            </Text>
          </View>
        </View>
      </View>

      {/* Contact Button */}
      <TouchableOpacity style={styles.contactButton} onPress={handleContactOwner}>
        <Text style={styles.contactButtonText}>Contact Owner</Text>
      </TouchableOpacity>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f9f9f9",
  },
  imageContainer: {
    flexDirection: "row",
  },
  image: {
    width: 300,
    height: 300,
    borderRadius: 10,
  },
  imageMargin: {
    marginRight:10,  // Gap of 5 between images
  },
  detailsContainer: {
    paddingVertical: 16,
    marginHorizontal: 16,
    marginBottom: 16,
  },
  title: {
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 8,
    color: "#333",
  },
  rent: {
    fontSize: 18,
    fontWeight: "600",
    color: "#4caf50",
    marginBottom: 8,
  },
  address: {
    fontSize: 16,
    color: "#666",
    marginBottom: 4,
  },
  pinCode: {
    fontSize: 16,
    color: "#666",
    marginBottom: 4,
  },
  dimensions: {
    fontSize: 16,
    color: "#666",
    marginBottom: 4,
  },
  accommodation: {
    fontSize: 16,
    color: "#666",
    marginBottom: 4,
  },
  amenitiesContainer: {
    padding: 16,
    backgroundColor: "#fff",
    borderRadius: 10,
    marginHorizontal: 16,
    marginBottom: 30, // Added space between amenities and button
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowRadius: 5,
    elevation: 3,
  },
  sectionHeader: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 12,
    color: "#333",
  },
  amenitiesList: {
    flexDirection: "row",
    justifyContent: "space-around",
    gap: 5,
  },
  amenity: {
    alignItems: "center",
    backgroundColor: "#f5f5f5",
    flex: 3,
    borderRadius: 5,
    padding: 2,
  },
  amenityText: {
    fontSize: 14,
    marginTop: 4,
    color: "#555",
    justifyContent: "center",
    alignItems: "center",
  },
  contactButton: {
    backgroundColor: "black",
    paddingVertical: 12,
    marginHorizontal: 16,
    marginBottom: 20,
    marginTop: 5,
    borderRadius: 10,
    alignItems: "center",
    elevation: 3,
  },
  contactButtonText: {
    fontSize: 18,
    color: "#fff",
    fontWeight: "bold",
  },
  loadingContainer:{
    flex:1
  }
});


export default RoomDetails;
