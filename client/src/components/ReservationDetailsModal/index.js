import axios from 'axios';
import PropTypes from 'prop-types';
import React, {Component} from 'react';
import {Button, Dropdown, Header, Icon, Form, Input, Modal, Checkbox, Tab} from 'semantic-ui-react';
import SweetAlert from 'sweetalert2-react';
import settings from '../../config/settings'
import {getTokenHeader} from '../../utils/requestHeaders';
import './ReservationDetailsModal.scss';
import {toDateInputValue} from '../../utils/dateFormatter';


class ReservationDetailsModal extends Component {
  state = {
    show: false,
    startHour: this.props.startHour,
    startMinute: this.props.startMinute,
    endHour: this.props.endHour,
    endMinute: this.props.endMinute,
    hourOptions: [],
    reservedOptions: [],
    modalTitle: '',
    modalText: '',
    modalType: 'success',
    isRecurring: false,
    tabIndex: 0,
    inputOption0: {
      startDate: toDateInputValue(this.props.selectedDate),
      endDate: null
    }
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
        text: `${i < 10 ? `0${i}` : i}`,
        value: `${i < 10 ? `0${i}` : i}`
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
      show: false,
    });
  }

  closeModalWithReservation = () => {
    this.props.onCloseWithReservation();
    this.setState({
      show: false,
    });
  }

  closeAlertModal = () => {
    const {modalType} = this.state;

    this.setState({
      showModal: false
    })

    // Handle successful reservation
    if (modalType === 'success') {
      this.closeModalWithReservation();
    }
  }

  handleOpen = () => this.setState({show: true});

  handleStartHourChange = (e, {value}) => {
    this.setState({
      startHour: value
    });
  }

  handleStartMinuteChange = (e, {value}) => {
    this.setState({
      startMinute: value
    });
  }

  handleEndHourChange = (e, {value}) => {
    this.setState({
      endHour: value
    });
  }

  handleEndMinuteChange = (e, {value}) => {
    this.setState({
      endMinute: value
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

  handleTabChange = (e, {activeIndex}) => {
    this.setState({tabIndex: activeIndex})
  }

  verifyRecurringOption0 = () => {
    const {startDate, endDate} = this.state.inputOption0;
    console.log('hhoura');
    if (endDate == null) {
      console.log(endDate);
      throw new Error('Please enter an end date.');
    }
  }

  handleSubmit = () => {
    let {tabIndex} = this.state;
    console.log(typeof (tabIndex));
    // Verify requirements before sending the POST request
    try {
      this.verifyEndTime();
      this.verifyReservationTimes();
      if (this.state.isRecurring) {
        switch (tabIndex) {
          case 0:
            this.verifyRecurringOption0()
            break;
          default:
            throw new Error('Something went wrong')
            break;
        }
        return;
      }
    }
    catch (err) {
      this.setState({
        showModal: true,
        modalTitle: 'Reservation blocked',
        modalText: err.message,
        modalType: 'warning'
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
        this.setState({
          showModal: true,
          modalTitle: 'Completed',
          modalText: `Room ${this.props.selectedRoomName} was successfuly booked.`,
          modalType: 'success'
        })
      })
      .catch((error) => {
        this.setState({
          showModal: true,
          modalTitle: 'Reservation failed',
          modalText: 'We are sorry, this reservation overlaps with other reservations. Try different times.',
          modalType: 'error'
        });
      })
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.show) {
      this.setState({
        show: nextProps.show
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
      if (nextProps.selectedHour.includes('PM') && hour !== '12') {
        hour = `${(parseInt(hour) + 12)}`;
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

  handleCheckboxClick = () => {
    let {isRecurring} = this.state;
    this.setState({isRecurring: !isRecurring})
  }

  handleStartDateChangeOption0 = (event) =>{this.setState({inputOption0:{startDate:event.target.value}}) }
  handleEndDateChangeOption0 = (event) =>{this.setState({inputOption0:{endDate:event.target.value}}) }

  renderRecurringBookingOption0 = () => {
    let {startDate} = this.state.inputOption0;
    return (
      <div>
        <div className="modal-description">
          <h3 className="header--inline">
            <Icon name="calendar alternate" /> {" "}
            {`Starting date`}
          </h3>
          <Form.Field>
            <Input
              size='small'
              icon='user'
              type="text"
              iconPosition='left'
              value={startDate}
              onChange={this.handleStartDateChangeOption0}
            />
          </Form.Field>
        </div>
        <div className="modal-description">
          <h3 className="header--inline">
            <Icon name="calendar alternate outline" /> {" "}
            {`End date `}
          </h3>
          <Form.Field>
            <Input
              size='small'
              icon='user'
              type="text"
              iconPosition='left'
              onChange={this.handleEndDateChangeOption0}
            />
          </Form.Field>
        </div>
      </div>
    )
  }

  renderRecurringForm() {
    const panes = [
      {menuItem: 'Option 1', render: () => <Tab.Pane attached={false}>{this.renderRecurringBookingOption0()}</Tab.Pane>},
      {menuItem: 'Option 2', render: () => <Tab.Pane attached={false}>Tab 2 Content</Tab.Pane>},
      {menuItem: 'Option 3', render: () => <Tab.Pane attached={false}>Tab 3 Content</Tab.Pane>},
    ]
    return (
      <div>
        <Tab menu={{pointing: true}} onTabChange={this.handleTabChange} panes={panes} />
      </div>
    )
  }

  renderDescription() {
    const {startHour, startMinute, hourOptions, minuteOptions, reservedOptions} = this.state;
    const {selectedDate} = this.props;
    return (
      <Modal.Content>
        <Modal.Description>
          <Header>
            <Icon name="calendar" />
            {selectedDate.toDateString()}
          </Header>
          <div className="modal-description">
            <h3 className="header--inline">
              <Icon className="hourglass start" />
              {`from `}
            </h3>
            <Dropdown
              selection
              compact
              placeholder='hh'
              className="dropdown--fixed-width"
              options={hourOptions}
              defaultValue={startHour}
              onChange={this.handleStartHourChange}
            />
            <Dropdown
              selection
              compact
              placeholder='mm'
              className="dropdown--fixed-width"
              options={minuteOptions}
              defaultValue={startMinute}
              onChange={this.handleStartMinuteChange}
            />
          </div>
          <div className="modal-description">
            <h3 className="header--inline">
              <Icon className="hourglass end" />
              {`to `}
            </h3>
            <Dropdown
              selection
              compact
              className="dropdown--fixed-width"
              placeholder='hh'
              options={hourOptions}
              onChange={this.handleEndHourChange}
            />
            <Dropdown
              selection
              compact
              className="dropdown--fixed-width"
              placeholder='mm'
              options={minuteOptions}
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
              options={reservedOptions}
              defaultValue={this.state.reservedOptions[0].value}
            />

          </div>
          <div className="modal-description">
            <Checkbox label='Request a recurring booking' onClick={this.handleCheckboxClick} />
          </div>
          {this.state.isRecurring ? this.renderRecurringForm() : null}
          <div className="ui divider" />
          <div>
            <Button content='Reserve' primary onClick={this.handleSubmit} />
            <Button content='Cancel' secondary onClick={this.closeModal} />
          </div>
        </Modal.Description>
      </Modal.Content>
    )
  }

  render() {
    const {show, showModal, modalTitle, modalText, modalType} = this.state;
    const {selectedRoomName} = this.props;
    return (
      <div id="reservation-details-modal">
        <Modal centered={false} size={"tiny"} open={show}>
          <Modal.Header>
            <Icon name="map marker alternate" />
            Room {selectedRoomName}
          </Modal.Header>
          {this.renderDescription()}
          <SweetAlert
            show={showModal}
            title={modalTitle}
            text={modalText}
            type={modalType}
            onConfirm={this.closeAlertModal}
          />
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
