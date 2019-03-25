import React, { Component } from 'react';
import {
  Button, Checkbox, Table, Segment,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';
import './EmailSettings.scss';


class EmailSettings extends Component {
  state = {
    whenBooking: false,
    whenInvitation: false,
    bookingReminder: false,
    whenCamponOnBooking: false,
    isLoading: false,
    disableButton: true,
  }

  componentDidMount() {
    this.syncSettings(this.getServiceToken());
  }

  getServiceToken = () => {
    // eslint-disable-next-line react/prop-types
    const { match } = this.props;
    let token;
    if (match !== undefined) {
      // eslint-disable-next-line prefer-destructuring
      token = match.params.token;
    }
    return token;
  }

  syncSettings = (token) => {
    this.setState({ isLoading: true });
    api.getEmailSettings(token)
      .then((r) => {
        if (r.status === 200) {
          this.setState({
            whenBooking: r.data.when_booking,
            whenInvitation: r.data.when_invitation,
            bookingReminder: r.data.booking_reminder,
            whenCamponOnBooking: r.data.when_camp_on_booking,
            isLoading: false,
          });
        }
      })
      .catch((e) => {
        const { data } = e.response;
        sweetAlert('Blocked', data.detail, 'error');
      });
  }

  handleWhenBookingOnToggle = (e, data) => {
    this.setState({
      whenBooking: data.checked,
      disableButton: false,
    });
  }


  handleWhenInvitationOnToogle = (e, data) => {
    this.setState({
      whenInvitation: data.checked,
      disableButton: false,
    });
  }

  handleBookingReminderOnToogle = (e, data) => {
    this.setState({
      bookingReminder: data.checked,
      disableButton: false,
    });
  }

  handleWhenCamponOnBookingOnToogle = (e, data) => {
    this.setState({
      whenCamponOnBooking: data.checked,
      disableButton: false,
    });
  }

  handleSaveOnClick = () => {
    const {
      whenBooking, whenInvitation,
      bookingReminder, whenCamponOnBooking,
    } = this.state;

    api.updateEmailSettings(
      whenBooking, whenInvitation,
      bookingReminder, whenCamponOnBooking, this.getServiceToken(),
    )
      .then((r) => {
        // console.log(r);
        if (r.status === 200) {
          this.sweetAlertSuccess();
          this.setState({
            disableButton: true,
          });
        }
      });
  }

  sweetAlertSuccess = () => {
    sweetAlert.fire({
      // position: 'top',
      type: 'success',
      title: 'Email settings saved',
      toast: true,
      showConfirmButton: false,
      timer: 2000,
    });
  }

  render() {
    const {
      whenBooking, whenInvitation,
      bookingReminder, whenCamponOnBooking, isLoading,
      disableButton,
    } = this.state;
    return (
      <div id="email-settings">
        <h1>Email Settings</h1>
        <Segment loading={isLoading}>
          <Table celled collapsing>
            <Table.Header>
              <Table.Row>
                <Table.HeaderCell>Email feature</Table.HeaderCell>
                <Table.HeaderCell />
              </Table.Row>
            </Table.Header>
            <Table.Body>
              <Table.Row>
                <Table.Cell>Receive email when making a booking</Table.Cell>
                <Table.Cell collapsing>
                  <Checkbox
                    toggle
                    checked={whenBooking}
                    onChange={this.handleWhenBookingOnToggle}
                  />
                </Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell>Receive email when invited to a group</Table.Cell>
                <Table.Cell collapsing>
                  <Checkbox
                    toggle
                    checked={whenInvitation}
                    onChange={this.handleWhenInvitationOnToogle}
                  />
                </Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell>Receive email reminder before a booking</Table.Cell>
                <Table.Cell collapsing>
                  <Checkbox
                    toggle
                    checked={bookingReminder}
                    onChange={this.handleBookingReminderOnToogle}
                  />
                </Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell>Receive email when someone camps on your booking</Table.Cell>
                <Table.Cell collapsing>
                  <Checkbox
                    toggle
                    checked={whenCamponOnBooking}
                    onChange={this.handleWhenCamponOnBookingOnToogle}
                  />
                </Table.Cell>
              </Table.Row>
            </Table.Body>
          </Table>
          <Button
            color="blue"
            onClick={this.handleSaveOnClick}
            disabled={disableButton}
          >
            Save
          </Button>
        </Segment>
      </div>
    );
  }
}

export default EmailSettings;
