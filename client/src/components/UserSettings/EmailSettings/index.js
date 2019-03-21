import React, { Component } from 'react';
import {
  Button, Checkbox, Table, Segment, Message,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';
import './EmailSettings.scss';


class EmailSettings extends Component {
  state = {
    whenBooking: false,
    whenDeleteBooking: false,
    whenDeleteRecurringBooking: false,
    whenCamponOnBooking: false,
    isLoading: false,
    showNeedToSaveMessage: false,
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
            whenDeleteBooking: r.data.when_delete_booking,
            whenDeleteRecurringBooking: r.data.when_delete_recurring_booking,
            whenCamponOnBooking: r.data.when_camp_on_booking,
            isLoading: false,
          });
        }
      })
      .catch((e) => {
        const { data } = e.response;
        console.log(data);
        sweetAlert('Blocked', data.detail, 'error');
      });
  }

  handleWhenBookingOnToggle = (e, data) => {
    this.setState({
      whenBooking: data.checked,
      showNeedToSaveMessage: true,
    });
  }


  handleWhenDeleteBookingOnToogle = (e, data) => {
    this.setState({
      whenDeleteBooking: data.checked,
      showNeedToSaveMessage: true,
    });
  }

  handleWhenDeleteRecurringBookingOnToogle = (e, data) => {
    this.setState({
      whenDeleteRecurringBooking: data.checked,
      showNeedToSaveMessage: true,
    });
  }

  handleWhenCamponOnBookingOnToogle = (e, data) => {
    this.setState({
      whenCamponOnBooking: data.checked,
      showNeedToSaveMessage: true,
    });
  }

  handleSaveOnClick = () => {
    const {
      whenBooking, whenDeleteBooking,
      whenDeleteRecurringBooking, whenCamponOnBooking,
    } = this.state;

    api.updateEmailSettings(
      whenBooking, whenDeleteBooking,
      whenDeleteRecurringBooking, whenCamponOnBooking, this.getServiceToken(),
    )
      .then((r) => {
        // console.log(r);
        if (r.status === 200) {
          this.sweetAlertSuccess();
          this.setState({
            showNeedToSaveMessage: false,
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
      whenBooking, whenDeleteBooking,
      whenDeleteRecurringBooking, whenCamponOnBooking, isLoading,
      showNeedToSaveMessage,
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
                <Table.Cell>Receive email when deleting a booking</Table.Cell>
                <Table.Cell collapsing>
                  <Checkbox
                    toggle
                    checked={whenDeleteBooking}
                    onChange={this.handleWhenDeleteBookingOnToogle}
                  />
                </Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell>Receive email when deleting a recurring booking</Table.Cell>
                <Table.Cell collapsing>
                  <Checkbox
                    toggle
                    checked={whenDeleteRecurringBooking}
                    onChange={this.handleWhenDeleteRecurringBookingOnToogle}
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
          {showNeedToSaveMessage ? (
            <Message warning>
              <Message.Header>Don&lsquo;t forget to click on Save button</Message.Header>
              {/* <p>Visit our registration page, then try again.</p> */}
            </Message>
          ) : null}
          <Button color="blue" onClick={this.handleSaveOnClick}>Save</Button>
        </Segment>
      </div>
    );
  }
}

export default EmailSettings;
