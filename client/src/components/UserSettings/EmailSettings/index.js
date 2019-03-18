import React, { Component } from 'react';
import {
  Button, Checkbox, Table, Segment,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';
// import PropTypes from 'prop-types';


class EmailSettings extends Component {
  state = {
    whenBooking: false,
    whenRecurringBooking: false,
    whenDeleteBooking: false,
    whenDeleteRecurringBooking: false,
    whenCamponOnBooking: false,
    isLoading: false,
  }

  componentDidMount() {
    // eslint-disable-next-line react/prop-types
    const { match } = this.props;
    let token;
    if (match !== undefined) {
      // eslint-disable-next-line prefer-destructuring
      token = match.params.token;
    }

    this.syncSettings(token);
  }

  syncSettings = (token) => {
    this.setState({ isLoading: true });
    if (token) {
      // TODO: sync settings with Auth token
      console.log(token);
    } else {
      api.getEmailSettings()
        .then((r) => {
          if (r.status === 200) {
            this.setState({
              whenBooking: r.data.when_booking,
              whenRecurringBooking: r.data.when_recurring_booking,
              whenDeleteBooking: r.data.when_delete_booking,
              whenDeleteRecurringBooking: r.data.when_delete_recurring_booking,
              whenCamponOnBooking: r.data.when_camp_on_booking,
              isLoading: false,
            });
          }
        });
    }
  }

  handleWhenBookingOnToggle = (e, data) => {
    this.setState({ whenBooking: data.checked });
  }

  handleWhenRecurringBookingOnToggle = (e, data) => {
    this.setState({ whenRecurringBooking: data.checked });
  }

  handleWhenDeleteBookingOnToogle = (e, data) => {
    this.setState({ whenDeleteBooking: data.checked });
  }

  handleWhenDeleteRecurringBookingOnToogle = (e, data) => {
    this.setState({ whenDeleteRecurringBooking: data.checked });
  }

  handleWhenCamponOnBookingOnToogle = (e, data) => {
    this.setState({ whenCamponOnBooking: data.checked });
  }

  handleSaveOnClick = () => {
    const {
      whenBooking, whenRecurringBooking, whenDeleteBooking,
      whenDeleteRecurringBooking, whenCamponOnBooking,
    } = this.state;

    api.updateEmailSettings(
      whenBooking, whenRecurringBooking, whenDeleteBooking,
      whenDeleteRecurringBooking, whenCamponOnBooking,
    )
      .then((r) => {
        // console.log(r);
        if (r.status === 200) {
          sweetAlert.fire({
            // position: 'top',
            type: 'success',
            title: 'Email settings saved',
            toast: true,
            showConfirmButton: false,
            timer: 2000,
          });
        }
      });
  }

  render() {
    const {
      whenBooking, whenRecurringBooking, whenDeleteBooking,
      whenDeleteRecurringBooking, whenCamponOnBooking, isLoading,
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
                <Table.Cell>Receive email when making a recurring booking</Table.Cell>
                <Table.Cell collapsing>
                  <Checkbox
                    toggle
                    checked={whenRecurringBooking}
                    onChange={this.handleWhenRecurringBookingOnToggle}
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
          <Button color="blue" onClick={this.handleSaveOnClick}>Save</Button>
        </Segment>
      </div>
    );
  }
}

export default EmailSettings;
