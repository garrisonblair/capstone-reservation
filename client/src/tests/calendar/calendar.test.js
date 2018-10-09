import React from 'react';
import renderer from 'react-test-renderer';
import Calendar from '../../components/Calendar/index';

it('Shows calendar', () => {
    const tree = renderer
        .create(<Calendar></Calendar>)
        .toJSON();
    expect(tree).toMatchSnapshot();
});
