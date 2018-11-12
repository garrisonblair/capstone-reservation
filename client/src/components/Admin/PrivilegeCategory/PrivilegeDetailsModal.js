import React, {Component} from 'react';
import {Button, Header, Icon, Modal} from 'semantic-ui-react';
import './PrivilegeDetailsModal.scss';


class PrivilegeDetailsModal extends Component {
  render() {
    return (
      <Modal className="privilege-details-modal" open={this.props.show} onClose={this.props.onClose}>
        <Header>
          {this.props.privilege.name}
        </Header>
        <div className="privilege-details-modal__container">
          <p>
            <strong> Name: </strong>
            {this.props.privilege.name}
          </p>
          <p>
          <strong> Parent Category: </strong>
            {this.props.privilege.parent_category || '-'}
          </p>
          <p>
            <strong> Max Days Until Booking: </strong>
            {this.props.privilege.max_days_until_booking}
          </p>
          <p>
            <strong> Max Bookings: </strong>
            {this.props.privilege.max_bookings}
          </p>
          <p>
            <strong> Max Recurring Bookings: </strong>
            {this.props.privilege.max_recurring_bookings}
          </p>
          <p>
            <strong> Recurring Booking Permission: </strong>
            {this.props.privilege.can_make_recurring_booking}
          </p>
          <p>
            <strong> Booking Start Time: </strong>
            {this.props.privilege.booking_start_time}
          </p>
          <p>
            <strong> Booking End Time: </strong>
            {this.props.privilege.booking_start_time}
          </p>
        </div>
        <div className="ui divider"/>
        <div className="controls">
          <Button icon labelPosition='left' negative size='small' onClick={this.props.onClose}>
            <Icon name='x' /> Close
          </Button>
        </div>
      </Modal>
    )
  }
}

export default PrivilegeDetailsModal;
