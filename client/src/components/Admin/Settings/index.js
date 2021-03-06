/* eslint camelcase: 0 */ // --> OFF
import React, { Component } from 'react';
import {
  Checkbox,
  Button,
  Input,
  Divider,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import WebCalendarLogin from './WebCalendarLogin';
import DisableBackupModal from './DisableBackupModal';
import api from '../../../utils/api';
import './Settings.scss';


class Settings extends Component {
  state = {
    showLoginModal: false,
    showDisableBackupModal: false,
    settings: {
      is_webcalendar_backup_active: false,
      merge_adjacent_bookings: false,
      merge_threshold_minutes: 0,
      booking_edit_lock_timeout: 0,
      group_can_invite_after_privilege_set: true,
      check_for_expired_bookings_active: false,
      campons_refutable: false,
      check_for_expired_bookings_frequency_seconds: 30,
      booking_time_to_expire_minutes: 30,
      manual_booking_confirmation: false,
      booking_reminders_active: false,
      default_time_to_notify_before_booking: 0,
    },
  }

  getSettings() {
    api.getAdminSettings()
      .then((response) => {
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

  handleChangeGroupInvitations = (e, data) => {
    const { checked } = data;
    const { settings } = this.state;
    settings.group_can_invite_after_privilege_set = checked;
    this.setState({
      settings,
    });
  }

  handleChangeMergeThreshold = (e, data) => {
    const { value } = data;
    const { settings } = this.state;
    settings.merge_threshold_minutes = value;
    this.setState({
      settings,
    });
  }

  handleBookingEditLock = (e, data) => {
    const { value } = data;
    const { settings } = this.state;
    settings.booking_edit_lock_timeout = value;
    this.setState({
      settings,
    });
  }

  handleCheckForExpiredBookings = (e, data) => {
    const { checked } = data;
    const { settings } = this.state;
    settings.check_for_expired_bookings_active = checked;
    this.setState({
      settings,
    });
  }

  handleCamponsRefutable = (e, data) => {
    const { checked } = data;
    const { settings } = this.state;
    settings.campons_refutable = checked;
    this.setState({
      settings,
    });
  }

  handleCheckForExpireBookingFrequency = (e, data) => {
    const { value } = data;
    const { settings } = this.state;
    settings.check_for_expired_bookings_frequency_seconds = value;
    this.setState({
      settings,
    });
  }

  handleManualBookingConfirmation = (e, data) => {
    const { checked } = data;
    const { settings } = this.state;
    settings.manual_booking_confirmation = checked;
    this.setState({
      settings,
    });
  }

  handleBookingExpirationThreshold = (e, data) => {
    const { value } = data;
    const { settings } = this.state;
    settings.booking_time_to_expire_minutes = value;
    this.setState({
      settings,
    });
  }

  handleChangeBookingRemindersActive = (e, data) => {
    const { checked } = data;
    const { settings } = this.state;
    settings.booking_reminders_active = checked;
    this.setState({
      settings,
    });
  }

  handleChangeDefaultTimeToNotifyBeforeBooking = (e, data) => {
    const { value } = data;
    const { settings } = this.state;

    settings.default_time_to_notify_before_booking = value;
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
      this.getSettings();
      sweetAlert('Save Successful', '', 'success');
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
      merge_threshold_minutes,
      booking_edit_lock_timeout,
      group_can_invite_after_privilege_set,
      check_for_expired_bookings_active,
      campons_refutable,
      check_for_expired_bookings_frequency_seconds,
      booking_time_to_expire_minutes,
      manual_booking_confirmation,
      booking_reminders_active,
      default_time_to_notify_before_booking,
    } = settings;

    return (
      <div>
        <div className="admin--settings">
          <h3>WebCalendar Backup</h3>
          <Checkbox
            className="settings_item"
            label="Automatically export to Web Calendar"
            checked={is_webcalendar_backup_active}
            onChange={this.handleChangeWebcaledarExport}
          />
          <Divider />
          <h3>Bookings</h3>
          <Checkbox
            className="settings_item"
            label="Merge adjacent bookings"
            checked={merge_adjacent_bookings}
            onChange={this.handleChangeMergeBooking}
          />
          <br />
          {merge_adjacent_bookings
            ? (
              <div>
                <Input
                  className="settings_item"
                  label="Merge threshold in minutes"
                  value={merge_threshold_minutes}
                  onChange={this.handleChangeMergeThreshold}
                />
                <br />
              </div>
            )
            : null
          }
          <Divider />
          <Input
            className="settings_item"
            label="Booking edit lock timeout"
            value={booking_edit_lock_timeout}
            onChange={this.handleBookingEditLock}
          />
          <Divider />
          <h3>Booking Confirmations and Card Readers</h3>
          <Checkbox
            className="settings_item"
            label="Bookings expire"
            checked={check_for_expired_bookings_active}
            onChange={this.handleCheckForExpiredBookings}
          />
          <Checkbox
            className="settings_item"
            label="Campons are Refutable"
            checked={campons_refutable}
            onChange={this.handleCamponsRefutable}
          />
          <Input
            className="settings_item"
            label="Booking expiration frequency (seconds)"
            value={check_for_expired_bookings_frequency_seconds}
            onChange={this.handleCheckForExpireBookingFrequency}
          />
          <Input
            className="settings_item"
            label="Time until bookings expire (minutes)"
            value={booking_time_to_expire_minutes}
            onChange={this.handleBookingExpirationThreshold}
          />
          <Checkbox
            className="settings_item"
            label="Allow confirmation from within application"
            checked={manual_booking_confirmation}
            onChange={this.handleManualBookingConfirmation}
          />
          <Divider />
          <h3>Groups</h3>
          <Checkbox
            className="settings_item"
            label="Allow group invitations after privilege validation"
            checked={group_can_invite_after_privilege_set}
            onChange={this.handleChangeGroupInvitations}
          />
          <Divider />
          <h3> Email Notifications </h3>
          <Checkbox
            className="settings_time"
            label="Booking Reminders active"
            checked={booking_reminders_active}
            onChange={this.handleChangeBookingRemindersActive}
          />
          <Input
            className="settings_item"
            label="Default time to notify before booking"
            value={default_time_to_notify_before_booking}
            onChange={this.handleChangeDefaultTimeToNotifyBeforeBooking}
          />
          <Divider />
          <Button onClick={this.saveSettings}>
            Save Changes
          </Button>
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
    );
  }
}

export default Settings;
