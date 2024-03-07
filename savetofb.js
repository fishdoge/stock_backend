// Import the functions you need from the SDKs you need
const { initializeApp } = require("firebase/app")
// const { getDatabase, set, child, get, push, update, ref } = require('firebase/database')
const { getFirestore } = require("firebase/firestore")
const {
  setDoc,
  doc,
  getDoc,
  collection,
  addDoc,
  getDocs,
  query,
  where,
  updateDoc,
  deleteDoc
} = require("firebase/firestore")
var fsp = require('fs/promises');
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAeKVIwpPOkxJTeoE7H2dmuuSQVomWPTok",
  authDomain: "virtual-stock-app-taimei.firebaseapp.com",
  projectId: "virtual-stock-app-taimei",
  storageBucket: "virtual-stock-app-taimei.appspot.com",
  messagingSenderId: "353840964544",
  appId: "1:353840964544:web:6783119eb35d3f8336de25"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getFirestore(app);


async function readData(path) {
  const dbRef = ref(getDatabase(app))
  const snapshot = await get(child(dbRef, path))
  try {
    if (snapshot.exists()) {
      const val = snapshot.val()
      console.log(val)
      return val
    } else {
      // console.log('No data available')
      return undefined
    }
  } catch {
    (error) => {
      console.log('viewUserData err')
      console.error(error)
    }
  }
}

// const r = readData('stockData')

 const getDataObj = async (qCollection) => {
  let users = {}

  const querySnapshot = await getDocs(
    collection(database, qCollection)
  );

  querySnapshot.forEach((doc) => {
    let i = doc.data()
    users[doc.id] = i
    // i.uid = doc.id
  });
  // console.log(querySnapshot.docs, "querySnapshot", users)
  var json = JSON.stringify(users);
  fsp.writeFile('backup_stockData.json', json, 'utf8');
  return users;
};
getDataObj('stockData')