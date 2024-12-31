import React from 'react';
import {
  View,
  Text,
  Image,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
} from 'react-native';

const { width } = Dimensions.get('window');

const PropertyCard = ({ room, onDelete, navigation}) => {
  const handleDelete = () => {
    if (onDelete) onDelete(room?.property_details?.[0]); // Pass property ID if available
  };

  const imageUrl =
    room?.property_photos?.[0]?.[2] || 'https://via.placeholder.com/100'; // Fallback image
  const propertyName =
    room?.property_details?.[2] || 'No property name available';
  const propertyPincode = room?.property_details?.[5] || 'N/A';
  const propertyRent = room?.property_details?.[3] || 'N/A';

  return (
    <TouchableOpacity  onPress={() => {
                    navigation.navigate('RoomDetails', { room });
                  }}>
      <View style={styles.featuredCard}>
        {/* Delete Button */}
        <TouchableOpacity
          style={styles.deleteButton}
          onPress={handleDelete}
          accessibilityLabel="Delete property">
          <Text style={styles.deleteButtonText}>X</Text>
        </TouchableOpacity>

        {/* Property Image */}
        <Image source={{ uri: imageUrl }} style={styles.roomImage} />

        {/* Property Details */}
        <View style={styles.roomInfo}>
          <Text style={styles.roomTitle}>{propertyName}</Text>
          <Text style={styles.roomSubtitle}>Pincode: {propertyPincode}</Text>
          <Text style={styles.roomSubtitle}>Rent: {propertyRent}</Text>
        </View>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  featuredCard: {
    flexDirection: 'row',
    marginBottom: 16,
    backgroundColor: '#FFF',
    borderRadius: 8,
    overflow: 'hidden',
    elevation: 3, // Adds shadow for Android
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    width: width - 32, // Adjust card width
    position: 'relative', // Required for absolute positioning
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
  deleteButton: {
    position: 'absolute',
    top: 8,
    right: 8,
    borderRadius: 20,
    padding: 8,
    zIndex: 10, // Ensures the button appears above other elements
  },
  deleteButtonText: {
    color: 'black',
    fontWeight: '600',
    fontSize: 12,
  },
});

export default PropertyCard;
