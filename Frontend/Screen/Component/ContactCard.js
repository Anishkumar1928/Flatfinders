import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Linking } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';

const ContactCard = ({phoneNumber}) => {
  const handleCall = () => {
    const mobNumber = `tel:${phoneNumber}`; // Replace with the desired phone number
    Linking.openURL(mobNumber).catch((err) =>
      console.error('Error opening phone number:', err)
    );
  };

  const handleWhatsAppChat = () => {
    const message = 'Hello, I need help!'; // Replace with your message
    const url = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;

    Linking.openURL(url).catch((err) =>
      console.error('Error opening WhatsApp chat:', err)
    );
  };

  return (
    <View style={styles.card}>
      <Text style={styles.title}>Contact Us</Text>
      <TouchableOpacity style={styles.button} onPress={handleCall}>
        <Icon name="phone" size={20} color="#fff" style={styles.icon} />
        <Text style={styles.buttonText}>Call Us</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.button} onPress={handleWhatsAppChat}>
        <Icon name="whatsapp" size={20} color="#fff" style={styles.icon} />
        <Text style={styles.buttonText}>Chat on WhatsApp</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 5,
    shadowOffset: { width: 0, height: 2 },
    elevation: 5,
    margin: 10,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'black',
    padding: 10,
    borderRadius: 5,
    marginVertical: 5,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    textAlign: 'center',
    marginLeft: 10,
  },
  icon: {
    marginRight: 10,
  },
});

export default ContactCard;
