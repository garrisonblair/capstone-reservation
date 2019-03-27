/* eslint-disable react/jsx-curly-spacing */
import React, { Component } from 'react';
import {
  Button, Table, Segment, Input,
} from 'semantic-ui-react';
import { ChromePicker } from 'react-color';
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
    displayBookingColorPicker: false,
    displayCamponColorPicker: false,
    displayPassedBookingColorPicker: false,
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

  handlePickBookingColor = (color) => {
    this.setState({
      bookingColor: color.hex,
      disableButton: false,
    });
  };

  handlePickCampOnColor = (color) => {
    this.setState({
      camponColor: color.hex,
      disableButton: false,
    });
  };

  handlePickPassedBookingColor = (color) => {
    this.setState({
      passedBookingColor: color.hex,
      disableButton: false,
    });
  };

  handleBookingColorClick = () => {
    const {
      displayBookingColorPicker,
    } = this.state;
    this.setState({ displayBookingColorPicker: !displayBookingColorPicker });
  };

  handleCampOnColorClick = () => {
    const {
      displayCamponColorPicker,
    } = this.state;
    this.setState({ displayCamponColorPicker: !displayCamponColorPicker });
  };

  handlePassedBookingColorClick = () => {
    const {
      displayPassedBookingColorPicker,
    } = this.state;
    this.setState({ displayPassedBookingColorPicker: !displayPassedBookingColorPicker });
  };

  handleBooingColorPickerClose = () => {
    this.setState({ displayBookingColorPicker: false });
  };

  handleCampOnColorPickerClose = () => {
    this.setState({ displayCamponColorPicker: false });
  };

  handlePassedBooingColorPickerClose = () => {
    this.setState({ displayPassedBookingColorPicker: false });
  };

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
      })
      .catch((e) => {
        const { data } = e.response;
        sweetAlert('Invalid Color Code', data.detail, 'error');
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
      bookingColor, camponColor, passedBookingColor,
      isLoading, disableButton,
      displayBookingColorPicker, displayCamponColorPicker, displayPassedBookingColorPicker
    } = this.state;
    const popover = {
      position: 'absolute',
      zIndex: '2',
    };
    const cover = {
      position: 'fixed',
      top: '0px',
      right: '0px',
      bottom: '0px',
      left: '0px',
    };
    return (
      <div id="personal-settings">
        <h1>Personal Settings</h1>
        <Segment loading={isLoading}>
          <Table celled collapsing>
            <Table.Header>
              <Table.Row>
                <Table.HeaderCell>Color title</Table.HeaderCell>
                <Table.HeaderCell>Color code (hex)</Table.HeaderCell>
                <Table.HeaderCell />
              </Table.Row>
            </Table.Header>
            <Table.Body>
              <Table.Row>
                <Table.Cell>Booking color</Table.Cell>
                <Table.Cell collapsing>
                  <Input
                    fluid
                    size="small"
                    iconPosition="left"
                    placeholder={bookingColor}
                    onChange={this.handleBookingColorChange}
                    onKeyPress={this.handleKeyPress}
                  />
                </Table.Cell>
                <Table.Cell collapsing>
                  <Button
                    color="grey"
                    onClick={this.handleBookingColorClick}
                  >
                    Choose color
                  </Button>
                  { displayBookingColorPicker
                    ? (
                      <div style={popover}>
                        <div
                          role="presentation"
                          style={cover}
                          onClick={this.handleBooingColorPickerClose}
                          onKeyDown={this.handleBooingColorPickerClose}
                        />
                        <ChromePicker
                          color={this.handlePickBookingColor}
                          onChangeComplete={this.handlePickBookingColor}
                        />
                      </div>) : null }
                </Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell>Campon color</Table.Cell>
                <Table.Cell collapsing>
                  <Input
                    fluid
                    size="small"
                    iconPosition="left"
                    placeholder={camponColor}
                    onChange={this.handleCamponColorChange}
                    onKeyPress={this.handleKeyPress}
                  />
                </Table.Cell>
                <Table.Cell collapsing>
                  <Button
                    color="grey"
                    onClick={this.handleCampOnColorClick}
                  >
                    Choose color
                  </Button>
                  { displayCamponColorPicker
                    ? (
                      <div style={popover}>
                        <div
                          role="presentation"
                          style={cover}
                          onClick={this.handleCampOnColorPickerClose}
                          onKeyDown={this.handleCampOnColorPickerClose}
                        />
                        <ChromePicker
                          color={this.handlePickCampOnColor}
                          onChangeComplete={this.handlePickCampOnColor}
                        />
                      </div>) : null }
                </Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell>Passed booking color</Table.Cell>
                <Table.Cell collapsing>
                  <Input
                    fluid
                    size="small"
                    iconPosition="left"
                    placeholder={passedBookingColor}
                    onChange={this.handlePassedBookingColorChange}
                    onKeyPress={this.handleKeyPress}
                  />
                </Table.Cell>
                <Table.Cell collapsing>
                  <Button
                    color="grey"
                    onClick={this.handlePassedBookingColorClick}
                  >
                    Choose color
                  </Button>
                  { displayPassedBookingColorPicker
                    ? (
                      <div style={popover}>
                        <div
                          role="presentation"
                          style={cover}
                          onClick={this.handlePassedBooingColorPickerClose}
                          onKeyDown={this.handlePassedBooingColorPickerClose}
                        />
                        <ChromePicker
                          color={this.handlePickPassedBookingColor}
                          onChangeComplete={this.handlePickPassedBookingColor}
                        />
                      </div>) : null }
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
