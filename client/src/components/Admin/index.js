import React, {Component} from 'react';
import {Button, Checkbox, Form, Input, Modal, Header} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import AdminRequired from '../HOC/AdminRequired';
import WebCalendarLogin from './WebCalendarLogin';
import api from '../../utils/api';
import './Admin.scss';


class Admin extends Component {

  state = {
    loginModal: false,
    webCalendarBackup: false
  }

  componentDidMount = () => {
    document.title = 'Capstone Settings'
    this.getSettings();
    this.setState({
      current: 'Settings'
    })
  }

  getSettings() {
    api.getAdminSettings()
    .then((response) => {
      this.setState({
        webCalendarBackup: response.data.is_webcalendar_backup_active
      })
    })
    .catch((error) => {
      console.log(error);
    })
  }

  disableBackup = (e) => {
    let data = {
      is_webcalendar_backup_active: false,
    }

    api.updateAdminSettings(data)
    .then((response) => {
      sweetAlert(
        'Completed',
        'Settings were successfuly saved.',
        'success'
      )
      this.toggleLoginModal();
    })
    .catch((error) => {
      console.log(error);
    })
  }

  handleClickNav = (e) => {
    let option = e.target.getAttribute('value');
    this.setState({current: option})
  }

  handleChangeSetting = (e, data) => {
    const {checked} = data;
    this.setState({
      webCalendarBackup: checked
    })

    this.toggleLoginModal();
  }

  toggleLoginModal = () => {
    this.setState({loginModal: !this.state.loginModal})
  }

  closeResponseModal = () => {
    this.setState({responseModal: !this.state.responseModal})
  }

  renderSettings() {
    return (
      <div className="admin__wrapper">
        <div>{this.renderNav()}</div>
        <div className="admin__content">
          {this.renderContent()}
        </div>
      </div>
    )
  }

  renderNav() {
    const {current} = this.state;
    const options = ['Settings', 'Stats']
    const menu = options.map((option) =>
      <li
        className={current == option? "active": ""}
        key={option}
        value={option}
        onClick={this.handleClickNav}
      >
          {option}
      </li>
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
    const {webCalendarBackup} = this.state
    return (
      <form onSubmit={this.saveSettings}>
        <label>
          Automatically export to Web Calendar
          <Checkbox
            checked={webCalendarBackup}
            onChange={this.handleChangeSetting}
          />
        </label>
        <br/>
        {/* <input type="submit" value="Save" /> */}
      </form>
    )
  }

  renderLoginModal() {
    const {webCalendarBackup} = this.state;

    let component = (
      <WebCalendarLogin
        show={this.state.loginModal}
        onClose={this.toggleLoginModal}
      />
    )

    if (!webCalendarBackup) {
      component = (
        <Modal open={this.state.loginModal} onClose={this.toggleLoginModal}>
          <Header>
            <h1 className="login__container__header__title">
              {'Disable automatic backup?'}
            </h1>
          </Header>
          <div className="login__container__main">
            <div className="ui divider"/>
            <div className="login__container__main__form-wrapper">
              <Form.Field>
                <Button fluid size='small' icon onClick={this.disableBackup}>
                  Confirm
                </Button>
              </Form.Field>
              <div className="ui divider"/>
            </div>
          </div>
        </Modal>
      )
    }

    return component;
  }

  render() {
    const {responseModal, responseModalText, responseModalTitle, responseModalType} = this.state
    return (
      <div id="admin">
        {this.renderSettings()}
        {this.renderLoginModal()}
      </div>
    )
  }
}

export default AdminRequired(Admin);
