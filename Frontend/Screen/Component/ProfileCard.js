// components/ProfileCard.js
import React, { useState, useContext } from 'react';
import {
  View,
  Modal,
  Text,
  Image,
  StyleSheet,
  TouchableOpacity,
} from 'react-native';
import { ContextApi } from '../ContextApi';

const ProfileCard = ({ navigation }) => {
  const { profile, logout } = useContext(ContextApi);
  const [popVisible, setpopVisible] = useState(false);
  return (
    <View style={styles.container}>
      {/* Profile Header */}
      <View style={styles.header}>
        <Image
          source={{
            uri: profile?.profilpic, // Replace with actual avatar URL
          }}
          style={styles.avatar}
        />
        <Text style={styles.name}>{profile.logged_in_as[1]}</Text>
        <Text style={styles.username}>{profile.logged_in_as[3]}</Text>
        <TouchableOpacity
          onPress={() =>
            navigation.navigate('UpdateProfile')
          }
          style={styles.editProfileButton}>
          <Text style={styles.editProfileText}>Edit Profile</Text>
        </TouchableOpacity>
      </View>

      {/* Options */}
      <View style={styles.optionsContainer}>
        <TouchableOpacity
          onPress={() => setpopVisible(true)}
          style={styles.option}>
          <Text style={styles.optionText}>veiw profile</Text>
          <Text style={styles.optionArrow}>›</Text>
        </TouchableOpacity>
        {profile.logged_in_as[6] === 'Owner' && (
          <TouchableOpacity
            onPress={() => navigation.navigate('MypropertyScreen')}
            style={styles.option}>
            <Text style={styles.optionText}>Your Properties</Text>
            <Text style={styles.optionArrow}>›</Text>
          </TouchableOpacity>
        )}
        <TouchableOpacity style={styles.option} onPress={() => navigation.navigate('ChangePassword')}>
          <Text style={styles.optionText}>Change password</Text>
          <Text style={styles.optionArrow}>›</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.option} onPress={logout}>
          <Text style={styles.optionText}>Logout</Text>
          <Text style={styles.optionArrow}>›</Text>
        </TouchableOpacity>
      </View>
      <View style={styles.centeredView}>
        <Modal
          animationType="slide"
          transparent={true}
          visible={popVisible}
          onRequestClose={() => {
            setpopVisible(!popVisible);
          }}>
          <View style={styles.centeredView}>
            <View style={styles.modalView}>
              <View style={styles.header}>
                <Image
                  source={{
                    uri: profile?.profilpic, // Replace with actual avatar URL
                  }}
                  style={styles.avatar}
                />
                <Text style={styles.name}>{profile.logged_in_as[1]}</Text>
                <Text style={styles.username}>{profile.logged_in_as[2]}</Text>
                <Text style={styles.username}>{profile.logged_in_as[3]}</Text>
                <Text style={styles.username}>{profile.logged_in_as[6]}</Text>
              </View>

              <TouchableOpacity
                style={[styles.button, styles.buttonClose]}
                onPress={() => setpopVisible(!popVisible)}>
                <Text style={styles.textStyle}>X</Text>
              </TouchableOpacity>
            </View>
          </View>
        </Modal>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
    paddingTop: 80,
  },
  header: {
    alignItems: 'center',
    marginBottom: 30,
  },
  avatar: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#D9D9D9',
  },
  name: {
    fontSize: 20,
    fontWeight: '600',
    marginTop: 10,
  },
  username: {
    fontSize: 16,
    color: 'gray',
    marginTop: 5,
  },
  editProfileButton: {
    marginTop: 10,
    paddingVertical: 8,
    paddingHorizontal: 20,
    backgroundColor: '#ECECEC',
    borderRadius: 5,
  },
  editProfileText: {
    color: 'black',
    fontWeight: '500',
  },
  optionsContainer: {
    marginTop: 20,
  },
  option: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    padding: 15,
    borderRadius: 10,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 5,
    elevation: 2,
  },
  optionText: {
    fontSize: 16,
  },
  optionArrow: {
    fontSize: 18,
    color: 'gray',
  },
  modalView: {
    margin: 20,
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 35,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  button: {
    borderRadius: 200,
    padding: 10,
  },
  textStyle: {
    color: 'black',
    fontWeight: 'bold',
    textAlign: 'center',
    fontSize: 20,
  },
});

export default ProfileCard;
