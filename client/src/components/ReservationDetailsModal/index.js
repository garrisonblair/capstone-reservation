import React, { Component } from 'react';
import settings from '../../config/settings';
import './ReservationDetailsModal.scss';
import { Button, Header, Modal, Dropdown, Message } from 'semantic-ui-react';
import axios from 'axios';
import { getTokenHeader } from '../../utils/requestHeaders';
import { withRouter } from 'react-router-dom';
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
    minHour: this.props.minHour || 8,
    maxHour: this.props.maxHour || 24,
    date: (new Date(this.props.date)) || "please provide a date",
    startHour: "8",
    startMinute: "00",
    endHour: 0,
    endMinute: 0,
    roomNumber: parseInt(this.props.roomNumber) || "please provide a room number",
    hourOptions: [],
    minuteOptions: [
      { text: '00', value: '00' },
      { text: '10', value: '10' },
      { text: '20', value: '20' },
      { text: '30', value: '30' },
      { text: '40', value: '40' },
      { text: '50', value: '50' }
    ],
    reservedOptions: [
      // here the value should be 'this.props.username'
      { text: 'me', value: 1 }
    ]
  }

  generateHourOptions(minHour, maxHour) {
    minHour = parseInt(minHour);
    maxHour = parseInt(maxHour);
    let result = [];
    for (var i = minHour; i < maxHour; i++) {
      result.push({ text: i + '', value: i + '' });
    }
    return result;
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.show) {
      this.setState({ modalOpen: nextProps.show });
    }

    let hour = "";
    let minute = "";
    if (nextProps.selectedHour != "") {
      hour = nextProps.selectedHour.charAt(0) == '0' ? nextProps.selectedHour.substring(1,2) :  nextProps.selectedHour.substring(0,2);
      minute = nextProps.selectedHour.substring(3,5);
    }
    this.setState({
      roomNumber: nextProps.selectedRoomId,
      startHour: hour,
      startMinute: minute,
      date: nextProps.selectedDate
    });
  }

  componentWillMount() {
    this.setState({
      hourOptions: this.generateHourOptions(this.state.minHour, this.state.maxHour)
    });
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
  handleStartHourChange = (e, { value }) => {
    this.setState({
      startHour: value,
      messageConfig: {
        hidden: true
      }
    });
  }
  handleStartMinuteChange = (e, { value }) => {
    this.setState({
      startMinute: value,
      messageConfig: {
        hidden: true
      }
    });
  }

  handleEndHourChange = (e, { value }) => {
    this.setState({
      endHour: value,
      messageConfig: {
        hidden: true
      }
    });
  }

  handleEndMinuteChange = (e, { value }) => {
    this.setState({
      endMinute: value,
      messageConfig: {
        hidden: true
      }
    });
  }

  verifyEndTime() {
    if (this.state.endHour === 0 || this.state.endMinute === 0) {
      throw new Error("Please provide an end time to make a reservation.");
    }
  }

  verifyReservationTimes() {
    const startTime = this.state.startHour + "." + this.state.startMinute;
    const endTime = this.state.endHour + "." + this.state.endMinute;

    if (parseFloat(startTime) > parseFloat(endTime)) {
      throw new Error("Please provide a start time that is before the end time to make a reservation.");
    }
  }

  handleReserve = () => {
    //This try catch verifies requirements before sending the POST request
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

    //Handle time zone
    let tzoffset = (this.state.date).getTimezoneOffset() * 60000; 
    let localISOTime = (new Date(this.state.date - tzoffset)).toISOString().slice(0, -1);

    const data = {
      "room": this.state.roomNumber,
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

        const { history } = this.props;

        console.log('Booked sucessfully')
        this.setState({
          messageConfig: {
            hidden: false,
            title: 'Completed',
            message: `Room ${this.state.roomNumber} was successfuly booked.`,
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
  modalDescription() {
    return <Modal.Content>
      <Modal.Description>
        <Header>Room {this.state.roomNumber} </Header>
        <p>Date: {this.state.date.toDateString()}</p>
        <br />
        <span>
          <span className="inputLabel">From:</span>
          <Dropdown placeholder='hh' onChange={this.handleStartHourChange} selection compact className="timeSelection" options={this.state.hourOptions} defaultValue={this.state.startHour} />
          <Dropdown placeholder='mm' onChange={this.handleStartMinuteChange} selection compact className="timeSelection" options={this.state.minuteOptions} defaultValue={this.state.startMinute} />
          <span className="inputLabel" id="toLabel">To:</span>
          <Dropdown placeholder='hh' onChange={this.handleEndHourChange} selection compact className="timeSelection" options={this.state.hourOptions} />
          <Dropdown placeholder='mm' onChange={this.handleEndMinuteChange} selection compact className="timeSelection" options={this.state.minuteOptions} />
        </span>
        <br /><br />
        <span>
          <span className="inputLabel">Reserved by:</span>
          <Dropdown compact placeholder='hh' selection options={this.state.reservedOptions} defaultValue={this.state.reservedOptions[0].value} />
        </span>
        <br /><br />
        <div>
          <Button content='Reserve' primary onClick={this.handleReserve} />
          <Button content='Cancel' secondary onClick={this.closeModal} />
        </div>
      </Modal.Description>
    </Modal.Content>
  }

  render() {
    return (
      <div id="reservation-details-modal">
        <Modal centered={false} size={"tiny"} open={this.state.modalOpen}>
          <Modal.Header>Reservation Details</Modal.Header>
          {this.state.messageConfig.color !== 'green' ? this.modalDescription() : null}
          <Message attached='bottom' color={this.state.messageConfig.color} hidden={this.state.messageConfig.hidden}>
            <Message.Header>{this.state.messageConfig.title}</Message.Header>
            <p>{this.state.messageConfig.message}</p>
          </Message>
        </Modal>
      </div>
    )
  }
}

export default ReservationDetailsModal;
// export default withRouter(ReservationDetailsModal)
