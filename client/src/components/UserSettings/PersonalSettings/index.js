import React, { Component } from 'react';
import {
  Button, Table, Segment,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';
import './PersonalSettings.scss';


class PersonalSettings extends Component {
  state = {
    bookingColor: '#1F5465',
    camponColor: '#82220E',
    passedBookingColor: '#7F7F7F',
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
    api.getPersonalSettings(token)
      .then((r) => {
        if (r.status === 200) {
          this.setState({
            bookingColor: r.data.booking_color,
            camponColor: r.data.campon_color,
            passedBookingColor: r.data.passed_booking_color,
            isLoading: false,
          });
        }
      })
      .catch((e) => {
        const { data } = e.response;
        sweetAlert('Blocked', data.detail, 'error');
      });
  }

  handleBookingColorChange = (event) => {
    this.setState({
      bookingColor: event.target.value,
      disableButton: false,
    });
  }

  handlePassedBookingColorChange = (event) => {
    this.setState({
      passedBookingColor: event.target.value,
      disableButton: false,
    });
  }

  handleCamponColorChange = (event) => {
    this.setState({
      camponColor: event.target.value,
      disableButton: false,
    });
  }

  handleSaveOnClick = () => {
    const {
      bookingColor, camponColor, passedBookingColor,
    } = this.state;

    api.updatePersonalSettings(
      bookingColor, camponColor, passedBookingColor, this.getServiceToken(),
    )
      .then((r) => {
        // console.log(r);
        if (r.status === 200) {
          this.sweetAlertSuccess();
          this.setState({
            disableButton: true,
          });
        } else {
          sweetAlert.fire({
            position: 'top',
            type: 'error',
            text: 'Invalid credentials',
          });
        }
      });
  }

  sweetAlertSuccess = () => {
    sweetAlert.fire({
      // position: 'top',
      type: 'success',
      title: 'Personal settings has been updated',
      toast: true,
      showConfirmButton: false,
      timer: 2000,
    });
  }

  render() {
    const {
      bookingColor, camponColor, passedBookingColor, isLoading,
      disableButton,
    } = this.state;
    return (
      <div id="personal-settings">
        <h1>Personal Settings</h1>
        <Segment loading={isLoading}>
          <Table celled collapsing>
            <Table.Header>
              <Table.Row>
                <Table.HeaderCell>Personalization</Table.HeaderCell>
                <Table.HeaderCell />
              </Table.Row>
            </Table.Header>
            <Table.Body>
              <Table.Row>
                <Table.Cell>Booking color</Table.Cell>
                <Table.Cell collapsing>
                  <input
                    type="text"
                    id="bookingColor"
                    value={bookingColor}
                    onChange={this.handleBookingColorChange}
                    onKeyPress={this.handleKeyPress}
                  />
                </Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell>Campon color</Table.Cell>
                <Table.Cell collapsing>
                  <input
                    type="text"
                    id="camponColor"
                    value={camponColor}
                    onChange={this.handleCamponColorChange}
                    onKeyPress={this.handleKeyPress}
                  />
                </Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell>Passed booking color</Table.Cell>
                <Table.Cell collapsing>
                  <input
                    type="text"
                    id="passedBookingColor"
                    value={passedBookingColor}
                    onChange={this.handlePassedBookingColorChange}
                    onKeyPress={this.handleKeyPress}
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

export default PersonalSettings;
