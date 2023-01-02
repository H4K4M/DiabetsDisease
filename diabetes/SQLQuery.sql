CREATE TABLE Hasta(
	HastaID int NOT NULL IDENTITY,
	Ad nvarchar(255),
	Soyad nvarchar(255),
	Eposta nvarchar(255) UNIQUE,
	PRIMARY KEY (HastaID)
);

CREATE TABLE Test(
	TestID int NOT NULL IDENTITY,
	HastaID int FOREIGN KEY REFERENCES Hasta(HastaID),
	GebelikSayisi int,
	GlikozSeviyesi int,
	KanBasinci int,
	DeriKalinligi int,
	InsulinSeviyesi int,
	VucutKitleEndeksi float,
	DiyabetSoyagaci float,
	Yas int,
	Tarih date,
	Sonuc bit
	PRIMARY KEY (TestID)
);

--Hasta Ekle Stored Procedure--
CREATE PROCEDURE HastaEkle @ad nvarchar(255), @soyad nvarchar(255), @eposta nvarchar(255)
AS
BEGIN
INSERT INTO Hasta
VALUES (@ad,@soyad,@eposta);
END

--  RNEK 1 --
EXEC HastaEkle @ad='Eren', @soyad='S me', @eposta = 'eren@some.com'

--Test Ekle Stored Procedure--
CREATE PROCEDURE TestEkle @hastaID int, @gebelik int, @glikoz int, @kan int, @deri int, @insulin int, @vke float, @soyagac float,
@yas int, @tarih date, @sonuc bit
AS
BEGIN
INSERT INTO Test
VALUES (@hastaID,@gebelik,@glikoz,@kan,@deri,@insulin,@vke,@soyagac,@yas,@tarih,@sonuc);
END

--  RNEK 2 --
EXEC TestEkle @hastaID=3, @gebelik=0, @glikoz=137, @kan=20, @deri=35, @insulin=168, @vke=43.1, @soyagac=2.288, @yas=22, @tarih='2022-12-31', @sonuc=1

select * from Hasta


--HastaTestGetir Stored Procedure--
CREATE PROCEDURE HastaTestGetir @eposta nvarchar(255)
AS
BEGIN
SELECT  t.TestID as 'Test Numaras ', h.Ad + ' ' + h.Soyad as 'Ad Soyad', t.Tarih as 'Test Tarihi', t.Sonuc as 'Test Sonucu'
FROM Hasta h, Test t
WHERE t.HastaID = h.HastaID
ORDER BY t.Tarih DESC
END

--  RNEK 3 --
EXEC HastaTestGetir @eposta = 'huseyink@gmail.com'


--BelirtilenSonucTestGetir--
CREATE PROCEDURE BelirtilenSonucTestGetir @sonuc bit
AS
BEGIN
SELECT t.TestID as 'Test Numaras ', h.Ad + ' ' + h.Soyad as 'Ad Soyad', t.Tarih as 'Test Tarihi', t.Sonuc as 'Test Sonucu'
FROM Hasta h, Test t
WHERE t.HastaID = h.HastaID AND t.Sonuc = @sonuc
ORDER BY 'Ad Soyad', t.Tarih DESC
END

--  RNEK 4 --
EXEC BelirtilenSonucTestGetir @sonuc = 1

--Test_Tarih Trigger--
CREATE TRIGGER Test_Tarih
ON Test
AFTER INSERT
AS
BEGIN
	UPDATE Test
	SET Tarih = GETDATE()
	WHERE Tarih IS NULL;
END