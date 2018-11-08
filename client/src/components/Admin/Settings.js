import React, {Component} from 'react';
import {Checkbox} from 'semantic-ui-react';
import WebCalendarLogin from './WebCalendarLogin';
import DisableBackupModal from './DisableBackupModal';
import api from '../../utils/api';
import './Admin.scss';


class Settings extends Component {
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
  }

  render() {
    const {webCalendarBackup, showLoginModal, showDisableBackupModal} = this.state;

    return (
      <div>
        <form onSubmit={this.saveSettings}>
          <div>
            <Checkbox
              label='Automatically export to Web Calendar'
              checked={webCalendarBackup}
              onChange={this.handleChangeSetting}
            />
          </div>
        </form>
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

export default Settings;
