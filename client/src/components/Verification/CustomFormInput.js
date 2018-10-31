import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Form, Input, Label} from 'semantic-ui-react';


class CustomFormInput extends Component {

  renderErrorMessage() {
    let component = '';
    if (this.props.errormessage) {
      component = (
        <div>
          <Label color="red" pointing='below'>
            {this.props.errormessage}
          </Label>
        </div>
      )
    }
    return component;
  }

  render() {
    return (
      <Form.Field>
        <label>{this.props.title}</label>
        {this.renderErrorMessage()}
        <Input
          {...this.props}
        />
      </Form.Field>
    )
  }
}

CustomFormInput.propTypes = {
  errormessage: PropTypes.string
}

export default CustomFormInput;
