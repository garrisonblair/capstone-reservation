/* eslint-disable no-undef */
import React from 'react';
import renderer from 'react-test-renderer';
import Bookers from '../../components/Admin/Bookers/index';

it('Shows bookers table', () => {
  const tree = renderer
    .create(
      <Bookers />,
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
