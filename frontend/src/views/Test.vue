<template>
  
</template>

<script>
export default {
  name: "Test",


  mounted() {
    this.test()
  },

  methods: {
    test() {
      const getPrice = new Promise(async (resolve, reject) => {
        // let fetchList = ['fetch', 'fetch2']
        // let dataItems = [];

        // fetchList.forEach(item => {
        //    this.fetch(item).then((data) => dataItems.push(data))
        // });

        for (let i=0; i<fetchList.length; i++) {
          await fetch(fetchList[i]).then((data) => dataItems.push(data))
        }
        resolve(dataItems)
      })

      getPrice.then((data) => {
        console.log(data)
      })
    },

    fetch(item) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve({'js': 'json'})
        }, 500)
      })
    }
  }
}
</script>

