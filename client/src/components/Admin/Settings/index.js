/* eslint camelcase: 0 */ // --> OFF
import React, { Component } from 'react';
import { Checkbox, Button, Input } from 'semantic-ui-react';
import WebCalendarLogin from './WebCalendarLogin';
import DisableBackupModal from './DisableBackupModal';
import api from '../../../utils/api';


class Settings extends Component {
  state = {
    showLoginModal: false,
    showDisableBackupModal: false,
    settings: {
      is_webcalendar_backup_active: false,
      merge_adjacent_bookings: false,
    },
  }

  getSettings() {
    api.getAdminSettings()
      .then((response) => {
        console.log('loaded');
        const settings = response.data;
        this.setState({ settings });
      });
  }

  handleChangeWebcaledarExport = (e, data) => {
    const { checked } = data;
    let showLoginModal = false;
    let showDisableBackupModal = false;

    if (checked) {
      showLoginModal = true;
    } else {
      showDisableBackupModal = true;
    }

    const { settings } = this.state;
    settings.webCalendarBackup = checked;

    this.setState({
      settings,
      showLoginModal,
      showDisableBackupModal,
    });
  }

  handleChangeMergeBooking = (e, data) => {
    const { checked } = data;
    const { settings } = this.state;
    settings.merge_adjacent_bookings = checked;
    this.setState({
      settings,
    });
  }

  handleCloseLoginModal = () => {
    this.setState({ showLoginModal: false });
    this.getSettings();
  }

  handleCloseDisableBackupModal = () => {
    this.setState({ showDisableBackupModal: false });
    this.getSettings();
  }

  componentDidMount = () => {
    document.title = 'Capstone Settings';
    this.getSettings();
  }

  saveSettings = () => {
    const { settings } = this.state;
    api.updateAdminSettings(settings).then(() => {
      console.log('Saved');
      this.getSettings();
    });
  }

  render() {
    const {
      showLoginModal,
      showDisableBackupModal,
      settings,
    } = this.state;

    const {
      is_webcalendar_backup_active,
      merge_adjacent_bookings,
    } = settings;

    return (
      <div>
        <form>
          <div>
            <Checkbox
              label="Automatically export to Web Calendar"
              checked={is_webcalendar_backup_active}
              onChange={this.handleChangeWebcaledarExport}
            />
            <Checkbox
              label="Merge adjacent bookings"
              checked={merge_adjacent_bookings}
              onChange={this.handleChangeMergeBooking}
            />
            <Input label="Merge threshold in minutes" />
          </div>
          <Button onClick={this.saveSettings}>
            Save Changes
          </Button>
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
    );
  }
}

export default Settings;
