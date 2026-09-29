from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.db import Base


class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    season = Column(String)
    description = Column(Text)

    growth_stages = relationship("GrowthStage", back_populates="crop")
    pests = relationship("PestDisease", back_populates="crop")


class GrowthStage(Base):
    __tablename__ = "growth_stages"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"))
    name = Column(String)
    order = Column(Integer)
    typical_duration_days = Column(String, nullable=True)

    crop = relationship("Crop", back_populates="growth_stages")


class PestDisease(Base):
    __tablename__ = "pests_diseases"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"))
    name = Column(String)
    type = Column(String)
    symptoms = Column(Text)
    affected_stage = Column(String, nullable=True)
    monitoring_method = Column(Text)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)

    crop = relationship("Crop", back_populates="pests")
    treatments = relationship("Treatment", back_populates="pest")


class Treatment(Base):
    __tablename__ = "treatments"

    id = Column(Integer, primary_key=True, index=True)
    pest_id = Column(Integer, ForeignKey("pests_diseases.id"))
    category = Column(String)
    method_name = Column(String)
    active_ingredient = Column(String, nullable=True)
    application_timing = Column(Text, nullable=True)
    dosage_note = Column(Text, default="Verify with product label")
    precautions = Column(Text)
    pre_harvest_interval_days = Column(Integer, nullable=True)
    is_verified = Column(String, default="demo")
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)

    pest = relationship("PestDisease", back_populates="treatments")


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    url = Column(String, nullable=True)
    publisher = Column(String)


class ProductPrice(Base):
    __tablename__ = "product_prices"

    id = Column(Integer, primary_key=True, index=True)
    treatment_id = Column(Integer, ForeignKey("treatments.id"))
    unit = Column(String)
    price_inr = Column(Float)
    updated_note = Column(String, default="user-editable estimate")