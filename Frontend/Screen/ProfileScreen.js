// screens/ProfileScreen.j
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import ProfileCard from './Component/ProfileCard';



const ProfileScreen = ({ navigation })=>{
   

  return (
    <ScrollView style={styles.container}>
      <ProfileCard style={styles.card} navigation={navigation} />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
});

export default ProfileScreen;
