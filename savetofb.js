// Import the functions you need from the SDKs you need
const { initializeApp } = require("firebase/app")
// const { getDatabase, set, child, get, push, update, ref } = require('firebase/database')
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
  deleteDoc,
  getFirestore
} = require("firebase/firestore")
var fsp = require('fs/promises');
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries
const axios = require('axios');

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
  const querySnapshot = await getDocs(collection(database, path));
  querySnapshot.forEach((doc) => {
    console.log(doc.id, " => ", doc.data());
  })

  // const dbRef = ref(getFirestore(app))
  // const snapshot = await get(child(dbRef, path))
  // try {
  //   if (snapshot.exists()) {
  //     const val = snapshot.val()
  //     console.log(val)
  //     return val
  //   } else {
  //     // console.log('No data available')
  //     return undefined
  //   }
  // } catch {
  //   (error) => {
  //     console.log('viewUserData err')
  //     console.error(error)
  //   }
  // }
}

// !
// const r = readData('stockData')
// console.log(r, "r")

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
  // console.log(users, users["123"])
  // var json = JSON.stringify(users);
  // fsp.writeFile('backup_users.json', json, 'utf8');
  return users;
};
//!                             
async function high_low() {
  const response = await axios.get(
    'https://hongwang-gcp.de.r.appspot.com/realtime',
  )
  const stockData = response.data;
  const datetime = new Date(stockData.time.datetime)
    .toISOString()
    .split('T')[0];
  // console.log(datetime,"datetime")
  const hldoc = getDataObj('high_low')
  if (hldoc[datetime]) { // update
    let i = {}
    if (stockData.tx.price > hldoc[datetime].high) {
      i = { high: stockData.tx.price, low: hldoc[datetime].low }
    } else if (stockData.tx.price < hldoc[datetime].low) {
      i = { high: hldoc[datetime].high, low: stockData.tx.price }
    }
    addData('high_low', datetime, i)
  } else { // add log
    let i = {}
    if (stockData.tx.open > stockData.tx.price) {
      i = { high: stockData.tx.open, low: stockData.tx.price }
    } else {
      i = { high: stockData.tx.price, low: stockData.tx.open }
    }
    addData('high_low', datetime, i)
  }
}
// high_low()//!


//!                               

const addData = async (collection, uid, data) => {
  // 指定 uid 作為 doc 的 id
  try {
    await setDoc(doc(database, collection, uid), data, { merge: true });
    console.log(collection + " " + uid + " addData: ", data)
  }
  catch (e) {
    console.log(e)
  }
};

// const yJSON = require("./get_tx_history/history/yield_tx_dow_22_23.json")
// const yJSON = require("./get_tx_history/history/yield_m_22_23.json")
async function uploadYieldJSON() {
  for (idx in yJSON['month_profit']) {
    let data = yJSON['month_profit'][idx]
    console.log(data)
    // addData("22_23_json", data.time, data)
    addData("yield_m_22_23", "month_profit", { [data.time]: data })
  }
  for (idx in yJSON['month_yield']) {
    let data = yJSON['month_yield'][idx]
    const yield = data['yield']
    data['yield'] = {}
    for (y in yield) {
      data['yield'][+y + 1] = yield[y]
      // console.log(y)
    }
    console.log(data)
    addData("yield_m_22_23", "month_yield", { [data.time]: data })
  }
}
// uploadYieldJSON()
// async function a() {
//   await setDoc(doc(database, "cities", "LA",),
//     {
//       oo: {
//         name: "Los Angeles",
//         state: "CA",
//         country: "USA"
//       }
//     })
// }
// a()

function formatStockData(stockData) {
  const tx = stockData.tx;
  const ym = stockData.ym;
  const txYmGap = stockData.tx_ym_gap;

  const high = Math.max(tx.open, tx.price); // ?
  const low = Math.min(tx.open, tx.price); // ?
  const buyPrice = tx.open;
  const sellPrice = tx.price;
  const profit = (sellPrice - buyPrice) * 200;
  const action = txYmGap >= 0 ? 'buy' : 'sell';

  let stop30 = null;
  let stop50 = null;
  if (profit > 6000) {
    stop30 = 6000;
  }
  if (profit < -6000) {
    stop30 = -6000;
  }
  if (profit > 10000) {
    stop50 = 10000;
  }
  if (profit < -10000) {
    stop50 = -10000;
  }

  const formattedDate = stockData.time.datetime.split('T')[0];

  return {
    '30_stop': stop30,
    '50_stop': stop50,
    action,
    buy_price: buyPrice,
    dow_percent: ym.percent,
    high,
    is_summer: false,
    low,
    percentage_gap: txYmGap,
    profit,
    sell_price: sellPrice,
    time: formattedDate,
    tx_percent: tx.percent,
  }
}

async function rename() {
  const json2223 = await getDataObj('yield_m_22_23')
  const reform = []
  for (let i in json2223.month_profit) {
    // console.log(i, json2223)
    reform.push({ time: i, profit: json2223.month_profit[i].profit, yield: json2223.month_yield[i].yield })
  }
  console.log(reform)
  for (let i in reform) {
    console.log(i, "i")
    addData("month_count", reform[i].time, reform[i])
  }
}
// !
// rename()

async function add_lost() {
  const stockData = await getDataObj('stockData')
  const transactions = await getDataObj('transactions')

  for (let key in stockData) {
    if (stockData[key].time) {
      if (stockData[key].time) {
        // console.log(key, stockData[key])
        if (!Object.keys(transactions).includes(key)) {
          const newForm = formatStockData(stockData[key])
          console.log(key, stockData[key], newForm)
          addData("transactions", key, newForm)
        }
      }
    }
  }
}
// !
// add_lost()



async function recount_PandY() {
  const month_count = await getDataObj('month_count')
  const transactions = await getDataObj('transactions')
  let py = {}

  /// count profit
  for (let date in transactions) {
    let year_mon = date.slice(0, 7)
    if (py[year_mon]) {
      py[year_mon].profit += transactions[date].profit
    } else {
      py[year_mon] = { profit: transactions[date].profit }
    }
  }
  /// count yield
  for (let year_mon in py) {
    if (month_count[year_mon]) { /// check if is in firebase
      if (month_count[year_mon].profit !== py[year_mon].profit) { /// do update
        let year = +(year_mon.slice(0, 4))
        let mon = +(year_mon.slice(5, 7))
        if (mon !== 1) {
          mon--
        } else {
          mon = 12
          year--
        }
        let last_record = year + "-" + mon.toFixed().padStart(2, '0')
        let updated = month_count[year_mon]
        updated.yield = month_count[last_record]
        for (let i = 1; i <= 5; i++) {
          updated.yield[i] += (py[year_mon].profit * i)
        }
        addData("month_count", year_mon, updated)
      }
    } else { /// count yield, add to firebase
      let year = +(year_mon.slice(0, 4))
      let mon = +(year_mon.slice(5, 7))
      if (mon !== 1) {
        mon--
      } else {
        mon = 12
        year--
      }
      let last_record = year + "-" + mon.toFixed().padStart(2, '0')
      py[year_mon].yield = py[last_record] ? py[last_record].yield : month_count[last_record].yield
      for (let i = 1; i <= 5; i++) {
        py[year_mon].yield[i] += (py[year_mon].profit * i)
      }
      console.log(py[year_mon].yield, py)
      py[year_mon].time = year_mon
      addData("month_count", year_mon, py[year_mon])
    }
  }
}
// !
// recount_PandY()

async function add_datetime() {
  const stockData = await getDataObj('stockData')
  const transactions = await getDataObj('transactions')

  for (let key in stockData) {
    let data = {}
    if (stockData[key].stockData) {
      data = stockData[key].stockData
    } else {
      data = stockData[key]
    }
    if (data.time) {
      let date_key = data.time.datetime.slice(0, 10)
      console.log(date_key)
      // console.log(transactions[date_key].time.length, date_key)
      if (transactions[date_key]) {
        if (transactions[date_key].time.length < 12) {
          // console.log(key, stockData[key])
          let new_trans = transactions[key]
          new_trans.time = stockData[key].time.datetime
          console.log(key, transactions[key], new_trans)
          // addData("transactions", key, new_trans)
        }
      }
    }
  }
}
// add_datetime() // !