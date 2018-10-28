import React, {Component} from 'react';
import settings from '../../config/settings';
import axios from 'axios';
import './Admin.scss';
import { Button } from 'semantic-ui-react';
import {getTokenHeader} from '../../utils/requestHeaders';


class Admin extends Component {

  state = {
    isAdmin: false
  }
  sweetAlert = require('sweetalert2');

  componentDidMount = () => {
    document.title = 'Capstone Settings'
    if(localStorage.getItem('CapstoneReservationUser')) {
      let user = JSON.parse(localStorage.getItem('CapstoneReservationUser'));
      if(user.is_superuser) {
        this.getSettings()
        this.setState({
          isAdmin: true,
          current: 'Settings'
        })
      }
    }
  }

  /************ REQUESTS *************/

  getSettings() {
    axios({
      method: 'GET',
      url: `${settings.API_ROOT}/settings`
    })
    .then((response) => {
      console.log(response.data)
      this.setState({
        webcalendar_backup: response.data.is_webcalendar_backup_active
      })
    })
    .catch(function (error) {
      console.log(error);
    })
    .then(function () {
      // always executed
    });
  }

  saveSettings = () => {
    console.log(this.state.webcalendar_backup)
    const headers = getTokenHeader();
    let data = {
      is_webcalendar_backup_active: this.state.webcalendar_backup ? 'true' : 'false'
    }
    axios({
      method: 'PATCH',
      url: `${settings.API_ROOT}/settings`,
      data,
      headers,
      withCredentials: true,
    })
    .then((response) => {
      this.sweetAlert('Completed',
          `Settings were successfuly saved.`,
          'success')
    })
    .catch(function (error) {
      console.log(error);
    })
    .then(function () {
      // always executed
    });
  }

  /************ CLICK HANDLING METHODS *************/

  handleClickNav = (e) => {
    let option = e.target.getAttribute('value');
    this.setState({current: option})
  }

  handleChangeSetting = (e) => {
    let setting = e.target.getAttribute('value');
    this.setState({[setting]: !this.state[setting]})
    console.log(this.state)
  }

  /************ COMPONENT RENDERING *************/

  renderSettings() {
    if(this.state.isAdmin) {
      return <div className="admin__wrapper"> <div>{this.renderNav()}</div><div className="admin__content">{this.renderContent()}</div></div>
    } else {
      return <div> NOT FOUND </div>
    }
  }

  renderNav() {
    const options = ['Settings', 'Stats']
    const menu = options.map((option) => 
      <li className={this.state.current == option ? "active" : ""} key={option} value={option} onClick={this.handleClickNav}>{option}</li>
    )
    return <ul className="admin__navigation">{menu}</ul>
  }

  renderContent() {
    const {current} = this.state
    let content
    switch (current) {
      case "Settings": 
        content = this.renderContentSettings()
        return content
      case "Stats":
        content = <div>Stats Content</div>;
        return content
    }
  }

  renderContentSettings() {
    return (
      <form onSubmit={this.saveSettings}>
        <label>
          Automatically export to Web Calendar
          <input type="checkbox" checked={!!this.state.webcalendar_backup} value="webcalendar_backup" onChange={this.handleChangeSetting} />
        </label>
        <br/>
        <input type="submit" value="Save" />
      </form>
    )
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
