import React, { useContext, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import PropertyCard from './Component/PropertyCard';
import { ContextApi } from './ContextApi';

export default function MypropertyScreen({ navigation }) {
  const { myproperty, getpropertybyid } = useContext(ContextApi);

  // Filter properties based on their availability
  const available = myproperty.filter(item => item.property_details[8] === true);
  const occupied = myproperty.filter(item => item.property_details[8] === false);

  useEffect(() => {
    getpropertybyid();
  }, []);

  return (
    <View style={styles.container}>
      {/* Scrollable Content */}
      <ScrollView style={styles.scrollContainer}>
        {/* Occupied Section */}
        <Text style={styles.sectionTitle}>OCCUPIED</Text>
        {occupied.map((item) => (
          <PropertyCard
            key={item.property_details[0]} // Ensure `property_details[0]` is the unique ID
            room={item} 
            navigation={navigation}// Pass the entire item as `room` prop
          />
        ))}

        {/* Available Section */}
        <Text style={styles.sectionTitle}>AVAILABLE</Text>
        {available.map((item) => (
          <PropertyCard
            key={item.property_details[0]} // Same here for the key
            room={item} 
            navigation={navigation}// Pass the entire item as `room` prop
          />
        ))}
      </ScrollView>

      {/* Fixed Add Button */}
      <TouchableOpacity
        onPress={() => navigation.navigate('propertyRegistration')}
        style={styles.addButton}
      >
        <Text style={styles.addButtonText}>+</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  scrollContainer: {
    flex: 1,
    padding: 16,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 8,
    color: 'black',
  },
  addButton: {
    backgroundColor: 'black',
    borderRadius: 50,
    width: 70,
    height: 70,
    justifyContent: 'center',
    alignItems: 'center',
    position: 'absolute', // Fix the button position
    bottom: 20, // 20px from the bottom
    right: 20, // 20px from the right
  },
  addButtonText: {
    color: 'white',
    fontSize: 24,
    fontWeight: 'bold',
  },
});
