import React, {Component} from 'react';
import {Checkbox} from 'semantic-ui-react';
import AdminRequired from '../HOC/AdminRequired';
import SideNav from './SideNav';
import WebCalendarLogin from './WebCalendarLogin';
import DisableBackupModal from './DisableBackupModal';
import api from '../../utils/api';
import './Admin.scss';


class Admin extends Component {

  state = {
    showLoginModal: false,
    showDisableBackupModal: false,
    webCalendarBackup: false
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

  handleCloseDisableBackupModal = () => {
    this.setState({showDisableBackupModal: false})
  }

  componentDidMount = () => {
    document.title = 'Capstone Settings'
    this.getSettings();
    this.setState({
      current: 'Settings'
    })
  }

  render() {
    const {webCalendarBackup, showLoginModal, showDisableBackupModal} = this.state;

    return (
      <div className="admin">
        <div className="admin__wrapper">
          <SideNav selectedMenu={'settings'}/>
          <div className="admin__content">
          <form onSubmit={this.saveSettings}>
            <label>
              Automatically export to Web Calendar
              <Checkbox
                checked={webCalendarBackup}
                onChange={this.handleChangeSetting}
              />
            </label>
          </form>
          </div>
        </div>
        <WebCalendarLogin
          show={showLoginModal}
          onClose={this.handleCloseLoginModal}
        />
        <DisableBackupModal
          show={showDisableBackupModal}
          onClose={this.handleCloseDisableBackupModal}
        />
      </div>
    )
  }
}

export default AdminRequired(Admin);
