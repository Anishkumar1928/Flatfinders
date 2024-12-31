import { useRef, useEffect } from 'react';
import { Button, StyleSheet, View, Text } from 'react-native';
import LottieView from 'lottie-react-native';

export default function Roomnotfound({ text }) {
  const animation = useRef<LottieView>(null);

  return (
    <View style={styles.animationContainer}>
      <Text style={styles.title}>{text}</Text>
      <LottieView
        autoPlay
        ref={animation}
        style={{
          width: 450,
          height: 450,
        }}
        source={require('../assets/Animation.json')}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  animationContainer: {
    backgroundColor: 'transparent', // Set the background to transparent
    alignItems: 'center',
    justifyContent: 'center',
    flex: 1,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: '#000',
    marginBottom: 16,
    textAlign: 'center',
  },
});
