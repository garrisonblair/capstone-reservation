import React, {Component} from 'react';
import settings from '../../config/settings';
import axios from 'axios';
import './Admin.scss';


class Admin extends Component {

  state = {
    isAdmin: false
  }

  componentDidMount = () => {
    document.title = 'Capstone Settings'
    if(localStorage.getItem('CapstoneReservationUser')) {
      let user = JSON.parse(localStorage.getItem('CapstoneReservationUser'));
      if(user.is_superuser) {
        this.setState({isAdmin: true})
        this.getSettings()
      }
    }
  }

  /************ REQUESTS *************/
  //TODO: Put correct url and handle response
  getSettings() {
    // axios({
    //   method: 'GET',
    //   url: `${settings.API_ROOT}/settings`
    // })
    // .then((response) => {

    // })
    // .catch(function (error) {
    //   console.log(error);
    // })
    // .then(function () {
    //   // always executed
    // });
  }


  /************ COMPONENT RENDERING *************/
  renderSettings() {
    if(this.state.isAdmin) {
      return <div> ADMIN </div>
    } else {
      return <div> NOT ADMIN </div>
    }
  }

  render() {
    return (
      <div>
        {this.renderSettings()}
      </div>     
    )
  }
}

export default Admin;
