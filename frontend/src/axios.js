import axios from 'axios';
import { Service } from 'axios-middleware';
import { mapState } from 'vuex'
import router from './router'

const service = new Service(axios);

service.register({
  onRequest(config) {
    return config;
  },
  onSync(promise) {
    return promise;
  },
  onResponseError(error) {
    console.log(error)
    if (error.response.status === 401) {
      // router.push('/login')
    } 
    throw(error)
  }
});
