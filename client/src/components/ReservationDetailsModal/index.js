import axios from 'axios';
import PropTypes from 'prop-types';
import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';
import {Button, Dropdown, Header, Icon, Message, Modal} from 'semantic-ui-react';
import settings from '../../config/settings'
import {getTokenHeader} from '../../utils/requestHeaders';
import './ReservationDetailsModal.scss';


class ReservationDetailsModal extends Component {

  state = {
    hideErrorMessage: true,
    messageConfig: {
      hidden: true,
      title: "",
      color: "red",
      message: ""
    },
    modalOpen: false,
    startHour: this.props.startHour,
    startMinute: this.props.startMinute,
    endHour: this.props.endHour,
    endMinute: this.props.endMinute,
    hourOptions: [],
    reservedOptions: []
  }

  generateHourOptions(minHour, maxHour) {
    let result = [];
    for (let i = minHour; i < maxHour; i++) {
      result.push({
        text: `${i}`,
        value: `${i}`
      });
    }
    return result;
  }

  generateMinuteOptions(minuteInterval) {
    let result = [];
    for (let i = 0; i < 60; i += minuteInterval) {
      result.push({
        text: `${i < 10? `0${i}`: i}`,
        value: `${i < 10? `0${i}`: i}`
      })
    }
    return result;
  }

  generateReservationProfilesOptions(reservationProfiles) {
    let result = reservationProfiles.map((profile) => ({text: profile, value: profile}))
    return result;
  }

  closeModal = () => {
    this.props.onClose();
    this.setState({
      modalOpen: false,
    });
  }

  closeModalWithReservation = () => {
    this.props.onCloseWithReservation();
    this.setState({
      modalOpen: false,
    });
  }

  handleOpen = () => this.setState({ modalOpen: true });

  handleStartHourChange = (e, {value}) => {
    this.setState({
      startHour: value,
      messageConfig: {
        hidden: true
      }
    });
  }

  handleStartMinuteChange = (e, {value}) => {
    this.setState({
      startMinute: value,
      messageConfig: {
        hidden: true
      }
    });
  }

  handleEndHourChange = (e, {value}) => {
    this.setState({
      endHour: value,
      messageConfig: {
        hidden: true
      }
    });
  }

  handleEndMinuteChange = (e, {value}) => {
    this.setState({
      endMinute: value,
      messageConfig: {
        hidden: true
      }
    });
  }

  verifyEndTime() {
    const {endHour, endMinute} = this.props;
    if (endHour.length === 0 || endMinute.length === 0) {
      throw new Error("Please provide an end time to make a reservation.");
    }
  }

  verifyReservationTimes() {
    const {startHour, startMinute, endHour, endMinute} = this.state;
    const startTime = `${startHour}.${startMinute}`;
    const endTime = `${endHour}.${endMinute}`;
    if (parseFloat(startTime) > parseFloat(endTime)) {
      throw new Error("Please provide a start time that is before the end time to make a reservation.");
    }
  }

  handleReserve = () => {
    // Verify requirements before sending the POST request
    try {
      this.verifyEndTime();
      this.verifyReservationTimes();
    }
    catch (err) {
      this.setState({
        messageConfig: {
          hidden: false,
          title: "Reservation blocked",
          message: err.message,
          color: "orange"
        }
      })
      return;
    }

    const headers = getTokenHeader();

    // Handle time zone
    let tzoffset = (this.props.selectedDate).getTimezoneOffset() * 60000;
    let date = new Date(this.props.selectedDate - tzoffset);
    let localISOTime = date.toISOString().slice(0, -1);

    const data = {
      "room": this.props.selectedRoomId,
      "date": localISOTime.slice(0, 10),
      "start_time": `${this.state.startHour}:${this.state.startMinute}:00`,
      "end_time": `${this.state.endHour}:${this.state.endMinute}:00`
    };

    axios({
      method: 'POST',
      url: `${settings.API_ROOT}/booking`,
      headers,
      data,
      withCredentials: true,
    })
    .then((response) => {
      // const {history} = this.props;
      console.log('Booked sucessfully')
      this.setState({
        messageConfig: {
          hidden: false,
          title: 'Completed',
          message: `Room ${this.props.selectedRoomId} was successfuly booked.`,
          color: 'green'
        }
      })
      // setTimeout(function () { history.push('/') }, 3300);
      this.closeModalWithReservation();
    })
    .catch((error) => {
      console.log(error.message);
      this.setState({
        messageConfig: {
          hidden: false,
          title: 'Reservation failed',
          message: 'We are sorry, this reservation overlaps with other reservations. Try different times.',
          color: "red"
        }
      });
    })
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.show) {
      this.setState({
        modalOpen: nextProps.show
      });
    }

    let hour = "";
    let minute = "";
    if (nextProps.selectedHour != "") {
      [hour, minute] = nextProps.selectedHour.replace('AM', '').replace('PM', '').trim().split(':');

      // Removes leading zero
      if (hour.charAt(0) === '0') {
        hour = hour.substring(1, 3);
      }

      // Handle 24-hour military time
      if (nextProps.selectedHour.includes('PM')) {
        hour = `${(parseInt(hour) + 12) % 24}`;
      }
    }
    this.setState({
      startHour: hour,
      startMinute: minute,
    });
  }

  componentWillMount() {
    const {minHour, maxHour, minuteInterval, reservationProfiles} = this.props;
    this.setState({
      hourOptions: this.generateHourOptions(minHour, maxHour),
      minuteOptions: this.generateMinuteOptions(minuteInterval),
      reservedOptions: this.generateReservationProfilesOptions(reservationProfiles)
    });
  }

  renderDescription() {
    return (
      <Modal.Content>
        <Modal.Description>
          <Header>
            <Icon name="calendar"/>
            {this.props.selectedDate.toDateString()}
          </Header>
          <div className="modal-description">
            <h3 className="header--inline">
              <Icon className="hourglass start"/>
              {`from `}
            </h3>
            <Dropdown
              selection
              compact
              placeholder='hh'
              className="dropdown--fixed-width"
              options={this.state.hourOptions}
              defaultValue={this.state.startHour}
              onChange={this.handleStartHourChange}
            />
            <Dropdown
              selection
              compact
              placeholder='mm'
              className="dropdown--fixed-width"
              options={this.state.minuteOptions}
              defaultValue={this.state.startMinute}
              onChange={this.handleStartMinuteChange}
            />
          </div>
          <div className="modal-description">
            <h3 className="header--inline">
              <Icon className="hourglass end"/>
              {`to `}
            </h3>
            <Dropdown
              selection
              compact
              className="dropdown--fixed-width"
              placeholder='hh'
              options={this.state.hourOptions}
              onChange={this.handleEndHourChange}
            />
            <Dropdown
              selection
              compact
              className="dropdown--fixed-width"
              placeholder='mm'
              options={this.state.minuteOptions}
              onChange={this.handleEndMinuteChange}
            />
          </div>
          <div className="modal-description">
            <h3 className="header--inline">
              <Icon name="user" /> {" "}
              {`by `}
            </h3>
            <Dropdown
              selection
              compact
              className="dropdown--fixed-width"
              placeholder='hh'
              options={this.state.reservedOptions}
              defaultValue={this.state.reservedOptions[0].value}
            />
          </div>
          <div className="ui divider"/>
          <div>
            <Button content='Reserve' primary onClick={this.handleReserve} />
            <Button content='Cancel' secondary onClick={this.closeModal} />
          </div>
        </Modal.Description>
      </Modal.Content>
    )
  }

  render() {
    return (
      <div id="reservation-details-modal">
        <Modal centered={false} size={"tiny"} open={this.state.modalOpen}>
          <Modal.Header>
            <Icon name="map marker alternate"/>
            Room {this.props.selectedRoomName}
          </Modal.Header>
          {this.state.messageConfig.color !== 'green'? this.renderDescription(): null}
          <Message attached='bottom' color={this.state.messageConfig.color} hidden={this.state.messageConfig.hidden}>
            <Message.Header>{this.state.messageConfig.title}</Message.Header>
            <p>{this.state.messageConfig.message}</p>
          </Message>
        </Modal>
      </div>
    )
  }
}

ReservationDetailsModal.propTypes = {
  show: PropTypes.bool.isRequired,
  selectedRoomId: PropTypes.string.isRequired,
  selectedRoomName: PropTypes.string.isRequired,
  selectedDate: PropTypes.object.isRequired,
  selectedHour: PropTypes.string.isRequired,
  minHour: PropTypes.number,
  maxHour: PropTypes.number,
  minuteInterval: PropTypes.number,
  onClose: PropTypes.func,
  onCloseWithReservation: PropTypes.func,
}

ReservationDetailsModal.defaultProps = {
  minHour: 8,
  maxHour: 24,
  minuteInterval: 10,
  startHour: "8",
  startMinute: "00",
  endHour: "-1",
  endMinute: "0",
  reservationProfiles: ['me']
}

export default ReservationDetailsModal;
