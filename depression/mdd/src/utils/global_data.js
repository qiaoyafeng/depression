var g_data = {
  id:1
}
import Vue from 'vue'

Vue.prototype.g_data_watch = (objItem, callback) => {

Object.defineProperty(g_data,objItem, {

get:function(){

returnthis.value

},

set:function(newValue){

this.value=newValue

callback(this.value)

}

})

}

export default g_data
