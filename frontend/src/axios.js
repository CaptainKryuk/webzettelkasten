import axios from 'axios';
import { Service } from 'axios-middleware';
import { mapState } from 'vuex' 

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
    return error
  }
});
