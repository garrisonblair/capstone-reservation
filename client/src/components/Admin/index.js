import React, {Component} from 'react';
import settings from '../../config/settings';
import axios from 'axios';
import './Admin.scss';
import {Button, Form, Modal, Input, Header} from 'semantic-ui-react';
import AdminRequired from '../HOC/AdminRequired';
import {getTokenHeader} from '../../utils/requestHeaders';


class Admin extends Component {

  state = {
    isAdmin: false,
    loginModal: false,
    webcalendarUsername: '',
    webcalendarPassword: ''
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
      this.setState({
        webcalendarBackup: response.data.is_webcalendar_backup_active
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
    const {webcalendarPassword, webcalendarUsername} = this.state
    const headers = getTokenHeader();
    let data = {
      is_webcalendar_backup_active: this.state.webcalendarBackup ? 'True' : 'False',
      webcalendar_username: webcalendarUsername,
      webcalendar_password: webcalendarPassword

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
      this.toggleLoginModal();
    })
    .catch(function (error) {
      console.log(error);
      if (error.message.includes('401')) {
        this.sweetAlert('Autenthication error',
          'The credentials you entered are invalid.',
          'error')
      }
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
    this.setState({[setting]: !this.state[setting]}, () => {
      if(setting == "webcalendarBackup") {
        console.log(this.state.webcalendarBackup)
        this.toggleLoginModal();
      }
    })
  }

  handleWebCalendarPasswordChange = (e) => {
    this.setState({webcalendarPassword: e.target.value})
  }

  handleWebCalendarUsernameChange = (e) => {
    this.setState({webcalendarUsername: e.target.value})
  }

  /************ HELPER METHOD *************/

  toggleLoginModal = () => {
    this.setState({loginModal: !this.state.loginModal})
  }

  closeResponseModal = () => {
    this.setState({responseModal: !this.state.responseModal})
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
          <input type="checkbox" checked={!!this.state.webcalendarBackup} value="webcalendarBackup" onChange={this.handleChangeSetting} />
        </label>
        <br/>
        {/* <input type="submit" value="Save" /> */}
      </form>
    )
  }

  renderCredentialsInputs() {
    return(
      <div>
        <Form.Field>
          <Input
            fluid
            size='small'
            icon='user'
            iconPosition='left'
            placeholder='Username'
            onChange={this.handleWebCalendarUsernameChange}
          />
        </Form.Field>
        <Form.Field>
          <Input
            fluid
            size='small'
            icon='lock'
            iconPosition='left'
            placeholder='Password'
            type='password'
            onChange={this.handleWebCalendarPasswordChange}
          />
        </Form.Field>
      </div>
    )
  }

  renderLoginModal() {
    return (
      <Modal open={this.state.loginModal} onClose={this.toggleLoginModal}>
          <Header>
            <h1 className="login__container__header__title"> { this.state.webcalendarBackup ? 'Please enter your Webcalendar credentials' : 'Disable automatic backup?'} </h1>
          </Header>
          <div className="login__container__main">
            <div className="ui divider"/>
            <div className="login__container__main__form-wrapper">
              {this.state.webcalendarBackup ? this.renderCredentialsInputs() : null}
              <Form.Field>
                <Button fluid size='small' icon onClick={this.saveSettings}>
                  Confirm
                </Button>
              </Form.Field>
              <div className="ui divider"/>
            </div>
          </div>
        </Modal>
    )
  }


  render() {
    const {responseModal, responseModalText, responseModalTitle, responseModalType} = this.state
    return (
      <div>
        {this.renderSettings()}
        {this.renderLoginModal()}
      </div>
    )
  }
}

export default AdminRequired(Admin);
