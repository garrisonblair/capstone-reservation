import React, {Component} from 'react';
import {Button, Checkbox, Form, Input, Modal, Header} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import AdminRequired from '../HOC/AdminRequired';
import SideNav from './SideNav';
import WebCalendarLogin from './WebCalendarLogin';
import api from '../../utils/api';
import './Admin.scss';


class Admin extends Component {

  state = {
    showLoginModal: false,
    showDisableBackupModal: false,
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
      this.setState({
        showDisableBackupModal: false
      })
    })
    .catch((error) => {
      console.log(error);
    })
  }

  handleChangeSetting = (e, data) => {
    const {checked} = data;
    let showLoginModal = false;
    let showDisableBackupModal = false;

    if (checked) {
      showLoginModal = true;
    } else {
      showDisableBackupModal = true;
    }

    this.setState({
      webCalendarBackup: checked,
      showLoginModal,
      showDisableBackupModal
    })
  }

  handleCloseLoginModal = () => {
    this.setState({showLoginModal: false})
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
      </form>
    )
  }

  renderLoginModal() {
    const {showLoginModal} = this.state;

    let component = (
      <WebCalendarLogin
        show={showLoginModal}
        onClose={this.handleCloseLoginModal}
      />
    )

    return component;
  }

  renderDisableBackupModal() {
    const {showDisableBackupModal} = this.state;

    let component = (
      <Modal open={showDisableBackupModal}>
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
    return component;
  }

  render() {
    return (
      <div className="admin">
        <div className="admin__wrapper">
          <SideNav selectedMenu={'settings'}/>
          <div className="admin__content">
            {this.renderContentSettings()}
          </div>
        </div>
        {this.renderLoginModal()}
        {this.renderDisableBackupModal()}
      </div>
    )
  }
}

export default AdminRequired(Admin);
