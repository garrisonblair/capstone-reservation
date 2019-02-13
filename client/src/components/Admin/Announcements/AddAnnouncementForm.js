import React, { Component } from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import {
  Form, TextArea, Button, Input,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';
import './AddAnnouncementForm.scss';

class AddAnnouncementForm extends Component {
  state = {
    subject: '',
    text: '',
    fromDate: moment().format('YYYY-MM-DD'),
    toDate: moment().format('YYYY-MM-DD'),
  }

  handleSubjectOnChange = (e, data) => { this.setState({ subject: data.value }); }

  handleTextOnChange = (e, data) => { this.setState({ text: data.value }); }

  handleFromDateOnChange = (e, data) => { this.setState({ fromDate: data.value }); }

  handleToDateOnChange = (e, data) => { this.setState({ toDate: data.value }); }

  isFormValid = () => {
    const {
      subject, text, fromDate, toDate,
    } = this.state;
    if (subject.length === 0) {
      sweetAlert('Blocked', 'Please add a Subject.', 'warning');
      return false;
    }
    if (text.length === 0) {
      sweetAlert('Blocked', 'Please add a message.', 'warning');
      return false;
    }
    if (new Date(fromDate) > new Date(toDate)) {
      sweetAlert('Blocked', 'End date should be after start date.', 'warning');
      return false;
    }

    return true;
  }

  handleAddButton = () => {
    const {
      subject, text, fromDate, toDate,
    } = this.state;
    if (!this.isFormValid()) {
      return;
    }
    const { syncFunction } = this.props;
    console.log(subject);
    console.log(text);
    console.log(fromDate);
    console.log(toDate);
    api.createAnnouncement(subject, text, fromDate, toDate)
      .then((r) => {
        if (r.status === 201) {
          syncFunction();
          this.setState({ subject: '', text: '' });
          sweetAlert('Success', 'Announcement was successfully created.', 'success');
        }
        console.log(r);
      });
  }

  render() {
    const {
      fromDate, text, toDate, subject,
    } = this.state;
    return (
      <div id="add-announcement-form">
        <Form>
          <Input
            placeholder="Title"
            className="subject-input"
            onChange={this.handleSubjectOnChange}
            value={subject}
          />
          <TextArea
            placeholder="Write announcement here"
            onChange={this.handleTextOnChange}
            value={text}
          />
        </Form>
        <div className="grid-container">
          <div className="from-date">
            From:
            <Input
              type="date"
              onChange={this.handleFromDateOnChange}
              size="small"
              value={fromDate}
            />
          </div>
          <div className="to-date">
            To:
            <Input
              type="date"
              onChange={this.handleToDateOnChange}
              size="small"
              value={toDate}
            />
          </div>
          <Button className="add-button" onClick={this.handleAddButton}>Add</Button>
        </div>
      </div>
    );
  }
}

AddAnnouncementForm.propTypes = {
  syncFunction: PropTypes.func.isRequired,
};

export default AddAnnouncementForm;
