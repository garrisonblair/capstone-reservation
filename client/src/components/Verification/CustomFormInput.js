import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Form, Input, Label } from 'semantic-ui-react';


class CustomFormInput extends Component {
  renderErrorMessage() {
    const { errormessage } = this.props;
    let component = '';
    if (errormessage) {
      component = (
        <div>
          <Label color="red" pointing="below">
            {errormessage}
          </Label>
        </div>
      );
    }
    return component;
  }

  render() {
    const { title } = this.props;
    return (
      <Form.Field>
        <label>{title}</label>
        {this.renderErrorMessage()}
        <Input
          {...this.props}
        />
      </Form.Field>
    );
  }
}

CustomFormInput.propTypes = {
  errormessage: PropTypes.string,
};

export default CustomFormInput;
