import React, { Component } from 'react';
import settings from '../../config/settings';
import './ReservationDetailsModal.scss';
import { Button, Header, Modal, Dropdown, Message } from 'semantic-ui-react';
import axios from 'axios';
import {getTokenHeader} from '../../utils/requestHeaders';
class ReservationDetailsModal extends Component {

  state = {
    hideErrorMessage: true,
    modalOpen: false,
    minHour: this.props.minHour || 8,
    maxHour: this.props.maxHour || 24,
    date: (new Date(this.props.date)) || "please provide a date",
    startHour: this.props.defaultHour + '',
    startMinute: this.props.defaultMinute + '',
    endHour:0,
    endMinute:0,
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

  componentWillMount() {
    this.setState({
      hourOptions: this.generateHourOptions(this.state.minHour, this.state.maxHour)
    });
  }

  closeModal = () => this.setState({
    modalOpen: false,
    hideErrorMessage: true
   });

  handleOpen = () => this.setState({ modalOpen: true });
  handleStartHourChange = (e, {value}) => this.setState({startHour: value});
  handleStartMinuteChange = (e, {value}) => this.setState({startMinute: value});
  handleEndHourChange = (e, {value}) => this.setState({endHour: value});
  handleEndMinuteChange = (e, {value}) => this.setState({endMinute: value});

  handleReserve = () => {
    const headers = getTokenHeader();

    const data = {
      "room": this.state.roomNumber,
      "date": this.state.date.toISOString().slice(0, 10),
      "start_time": `${this.state.startHour}:${this.state.startMinute}:00`,
      "end_time": "15:00:00"
    };
    console.log(data);
    axios({
      method: 'POST',
      url: `${settings.API_ROOT}/booking`,
      headers,
      data,
      withCredentials: true,
    })
    .then((response) => {
      console.log(response);

    })
    .catch((error) =>{
      console.log(error.message);
      this.setState({
        hideErrorMessage: false
      });
    })
  }

  render() {
    return (
      <div id="reservation-details-modal">
        <Modal trigger={<div onClick={this.handleOpen}>Click me</div>} centered={false} size={"tiny"} open={this.state.modalOpen}>
          <Modal.Header>Reservation Details</Modal.Header>
          <Message negative hidden={this.state.hideErrorMessage}>
            <Message.Header>Reservation failed</Message.Header>
            <p>We are sorry, this reservation overlaps with other reservations. Try different times.</p>
          </Message>
          <Modal.Content>
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
        </Modal>
      </div>
    )
  }
}

export default ReservationDetailsModal;
